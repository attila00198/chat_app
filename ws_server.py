import ssl
import json
import configparser
import websockets
from typing import Optional
from pydantic import ValidationError
from logging_config import setup_logging
from message_handler import MessageHandler, Message
from client_manager import ClientManager


class WebSocketServer:
    def __init__(self, config_path: str = 'config.ini'):
        # Konfiguráció betöltése
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Logger beállítása
        self.logger = setup_logging("WSServer")

        # Komponensek inicializálása
        self.client_manager = ClientManager()
        self.message_handler = MessageHandler()

        # SSL konfiguráció
        self.ssl_context = self._setup_ssl()

    def _setup_ssl(self) -> Optional[ssl.SSLContext]:
        """SSL kontextus beállítása a konfiguráció alapján"""
        use_ssl = self.config.getboolean('ssl', 'use_ssl')

        if not use_ssl:
            return None

        ssl_certfile = self.config['ssl']['ssl_certfile']
        ssl_keyfile = self.config['ssl']['ssl_keyfile']

        if not (ssl_certfile and ssl_keyfile):
            raise FileNotFoundError("SSL tanúsítványok és kulcsok nem találhatóak!")

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)
        return ssl_context

    async def handle_client(self, websocket):
        """Egyedi kliens kapcsolat kezelése"""
        username = None
        try:
            # Felhasználónév bekérése
            await websocket.send(
                json.dumps({"type": "nickname_request", "sender": "System", "content": "!NICKNAME"})
            )
            username = await websocket.recv()

            # Kliens regisztrálása
            await self.client_manager.add_client(username, websocket)
            await self.message_handler.broadcast_message("System", f"{username} joined the chat.")

            # Üzenetek fogadása és kezelése
            async for message in websocket:
                try:
                    parsed_message = Message.model_validate_json(message)
                    await self.message_handler.handle_message(parsed_message)
                except ValidationError as e:
                    self.logger.error(f"Invalid message format from {username}: {e}")
                    await websocket.send(
                        json.dumps({"type": "error", "content": "Invalid message format"})
                    )

        except websockets.ConnectionClosed:
            self.logger.info(f"Connection closed by {username}")
        finally:
            if username:
                self.logger.info(f"Client '{username}' disconnected")
                await self.client_manager.remove_client(username)
                await self.message_handler.broadcast_message("System", f"{username} disconnected.")

    async def start(self, host: str, port: int):
        """Szerver indítása a megadott host és port címen"""
        server = await websockets.serve(
            self.handle_client,
            host,
            port,
            ssl=self.ssl_context
        )

        self.logger.info(f"WebSocket server started on {host}:{port}")
        await server.wait_closed()

    def run(self, host: str, port: int):
        """Szinkron wrapper az aszinkron start metódushoz"""
        import asyncio
        asyncio.run(self.start(host, port))
