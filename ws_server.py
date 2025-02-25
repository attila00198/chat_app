import ssl
import configparser
import websockets
from typing import Optional
from pydantic import ValidationError
from logging_config import setup_logging
from message_handler import MessageHandler
from models import Message
from client_manager import ClientManager


class WebSocketServer:
    def __init__(self, config_path: str):
        # Konfiguráció betöltése
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Logger setup
        self.logger = setup_logging("Server")

        # Initializing components
        self.client_manager = ClientManager()
        self.message_handler = MessageHandler()

        # SSL configuration
        self.ssl_context = self._setup_ssl()

    def _setup_ssl(self) -> Optional[ssl.SSLContext]:
        """Setting up SSL context if SSL is enabled"""
        use_ssl = self.config.getboolean("ssl", "use_ssl")

        if not use_ssl:
            return None

        ssl_certfile = self.config["ssl"]["ssl_certfile"]
        ssl_keyfile = self.config["ssl"]["ssl_keyfile"]

        if not (ssl_certfile and ssl_keyfile):
            raise FileNotFoundError("SSL tanúsítványok és kulcsok nem találhatóak!")

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)
        return ssl_context

    async def handle_client(self, websocket):
        """Handleing client connections"""
        nickname = None
        try:
            # Felhasználónév bekérése
            NICKNAME_REQUEST = Message(
                type="system", sender="System", content="!NICKNAME"
            ).model_dump_json()

            await websocket.send(NICKNAME_REQUEST)
            nickname = await websocket.recv()

            # Registering client
            await self.client_manager.add_client(nickname, websocket)

            # Welcome message and broadcast user list
            self.logger.info(f"Client '{nickname}' connected")

            await self.message_handler.send_user_list()
            await self.message_handler.broadcast_message(
                Message(
                    type="system", sender="System", content=f"{nickname} connected."
                )
            )
            await websocket.send(
                Message(
                    type="system",
                    sender="System",
                    content="Welcome to the chat!\nUse /help to list all available commands.",
                ).model_dump_json()
            )

            # Receive and handle messages
            async for message in websocket:
                try:
                    parsed_message = Message.model_validate_json(message)
                    await self.message_handler.dispatch_message(parsed_message)
                except ValidationError as e:
                    self.logger.error(f"Invalid message format from {nickname}: {e}")
                    error_msg = Message(
                        type="error", sender="System", content="Invalid message format"
                    )
                    await websocket.send(error_msg.model_dump_json())

        except websockets.ConnectionClosed:
            self.logger.info(f"Connection closed by {nickname}")
        finally:
            # Handling client disconnection
            if nickname:
                self.logger.info(f"Client '{nickname}' disconnected")
                await self.client_manager.remove_client(nickname)
                await self.message_handler.broadcast_message(
                    Message(
                        type="system",
                        sender="System",
                        content=f"{nickname} disconnected.",
                    )
                )

    async def start(self, host: str, port: int):
        """Szerver indítása a megadott host és port címen"""
        server = await websockets.serve(
            self.handle_client, host, port, ssl=self.ssl_context
        )

        self.logger.info(f"WebSocket server started on {host}:{port}")
        await server.wait_closed()

    def run(self, host: str, port: int):
        """Szinkron wrapper az aszinkron start metódushoz"""
        import asyncio

        asyncio.run(self.start(host, port))
