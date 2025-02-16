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

# SSL beállítások
use_ssl = config.getboolean('ssl', 'use_ssl')  # boolean érték

# SSL kontextus létrehozása, ha szükséges
if use_ssl:
    ssl_certfile = config['ssl']['ssl_certfile']
    ssl_keyfile = config['ssl']['ssl_keyfile']

    # Ellenőrizni, hogy léteznek-e az SSL fájlok
    if not (ssl_certfile and ssl_keyfile):
        raise FileNotFoundError("SSL tanúsítványok és kulcsok nem találhatóak!")
    
    # SSL kontextus létrehozása
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)
else:
    ssl_context = None  # Ha nem használunk SSL-t, null értékre állítjuk

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
    if use_ssl:
        server = await websockets.serve(handle_client, host, port, ssl=ssl_context)
    else:
       server = await websockets.serve(handle_client, host, port) 
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()
