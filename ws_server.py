import json
import websockets
from logging_config import setup_logging
from message_handler import MessageHandler, Message
from client_manager import ClientManager
from pydantic import ValidationError

# Configure logging
logger = setup_logging("ws_server")

client_manager = ClientManager()
message_handler = MessageHandler()


async def handle_client(websocket):
    try:
        # Kérjük el a felhasználó nevét
        await websocket.send(
            json.dumps({"type": "system", "content": "!NICKNAME"})
        )
        username = await websocket.recv()
        print(username)

        # Regisztráljuk a felhasználót
        await client_manager.add_client(username, websocket)
        await message_handler.broadcast_message("SERVER", f"{username} connected.")

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
        logger.warning(f"Connection closed by {username}")
    finally:
        await client_manager.remove_client(username)
        logger.info(f"Client {username} disconnected")
        await message_handler.broadcast_message("SERVER", f"{username} disconnected.")


async def start_ws_server(host, port):
    server = await websockets.serve(handle_client, host, port)
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()
