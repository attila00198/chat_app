import websockets
import asyncio
from client_manager import ClientManager
from command_manager import CommandManager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('ws_server')

command_manager = CommandManager()
client_manager = ClientManager()

async def handle_client(websocket):
    try:
        await websocket.send("!NICKNAME")
        username = await websocket.recv()
        await client_manager.add_client(username, websocket)

        # Értesítsük a többi klienst az új felhasználó csatlakozásáról
        await broadcast_message("[SERVER]:", f"{username} connected.")

        async for message in websocket:
            if message.startswith("/"):
                await command_manager.handle_command(username, message)
            else:
                await broadcast_message(username, message)
    except websockets.ConnectionClosed:
        logger.warning(f"Connection closed by {username}")
    finally:
        await client_manager.remove_client(username)
        logger.info(f"Client {username} disconnected from WebSocket.")

        # Értesítsük a többi klienst a felhasználó kilépéséről
        await broadcast_message("[SERVER]", f"{username} disconnected.")

async def broadcast_message(sender_username, message):
    """Üzenet küldése minden kliensnek, kivéve azt, aki küldte."""
    message_to_send = f"{sender_username}: {message}"
    user_dict = await client_manager.get_all_user()
    for user, client_socket in user_dict.items():
        if user != sender_username:
            try:
                await client_socket.send(message_to_send)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")

async def start_ws_server(host, port):
    server = await websockets.serve(handle_client, host, port)
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()