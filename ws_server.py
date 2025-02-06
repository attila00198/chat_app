import websockets
from client_manager import client_manager
from message_handler import MessageHandler
from command_manager import CommandManager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('ws_server')

message_handler = MessageHandler(client_manager)
command_manager = CommandManager()

async def handle_client(websocket):
    try:
        await websocket.send("!NICKNAME")
        username = await websocket.recv()
        client_manager.add_client(username, websocket)
        logger.info(f"Client {username} connected to the server.")

        # Értesítsük a többi klienst az új felhasználó csatlakozásáról
        await message_handler.broadcast_message("[SERVER]", f"{username} connected.")

        async for message in websocket:
            if message.startswith("/"):
                await command_manager.handle_command(username, message)
            else:
                await message_handler.broadcast_message(username, message)
    except websockets.ConnectionClosed:
        logger.warning(f"Connection closed by {username}")
    finally:
        client_manager.remove_client(username)
        logger.info(f"Client {username} disconnected from WebSocket.")

        # Értesítsük a többi klienst a felhasználó kilépéséről
        await message_handler.broadcast_message("[SERVER]", f"{username} disconnected.")

async def start_ws_server(host, port):
    server = await websockets.serve(handle_client, host, port)
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()