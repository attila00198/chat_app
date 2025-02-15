import ssl
import json
import configparser
import websockets
from logging_config import setup_logging
from message_handler import MessageHandler, Message
from client_manager import ClientManager
from pydantic import ValidationError

config = configparser.ConfigParser()
config.read('config.ini')

# SSL
ssl_certfile = config['ssl']['ssl_certfile']
ssl_keyfile = config['ssl']['ssl_keyfile']

# Create ssl context
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)

# Configure logging
logger = setup_logging("ws_server", "ws_server.log")

client_manager = ClientManager()
message_handler = MessageHandler()


async def handle_client(websocket):
    try:
        # Kérjük el a felhasználó nevét
        await websocket.send(
            json.dumps({"type": "System", "sender": "System", "content": "!NICKNAME"})
        )
        username = await websocket.recv()

        # Regisztráljuk a felhasználót
        await client_manager.add_client(username, websocket)
        await message_handler.broadcast_message("System", f"{username} joined the chat.")

        async for message in websocket:
            try:
                # JSON feldolgozás Pydantic segítségével
                parsed_message = Message.model_validate_json(message)

                # Továbbítjuk a validált üzenetet a MessageHandlernek
                await message_handler.handle_message(parsed_message)

            except ValidationError as e:
                logger.error(f"Invalid message format from {username}: {e}")
                await websocket.send(
                    json.dumps({"type": "error", "content": "Invalid message format"})
                )

    except websockets.ConnectionClosed:
        logger.info(f"Connection closed by {username}")
    finally:
        logger.info(f"Client '{username}' disconnected")
        await client_manager.remove_client(username)
        await message_handler.broadcast_message("System", f"{username} disconnected.")



async def start_ws_server(host, port):
    server = await websockets.serve(handle_client, host, port, ssl=ssl_context)
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()
