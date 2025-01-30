import websockets
from client_manager import client_manager
from message_handler import MessageHandler
from logging_config import setup_logging

# Configure logging
logger = setup_logging('ws_server')

mh = MessageHandler(client_manager)

async def handle_client(websocket):
    try:
        await websocket.send("!NICKNAME")
        username = await websocket.recv()
        client_manager.add_client(username, websocket, 'websocket')
        logger.info(f"Client {username} connected via WebSocket.")

        # Értesítsük a többi klienst az új felhasználó csatlakozásáról
        await mh.handle_message("[SERVER]", f"{username} connected.")

        async for message in websocket:
            await mh.handle_message(username, message)
    except websockets.ConnectionClosed:
        logger.warning(f"Connection closed by {username}")
    finally:
        client_manager.remove_client(username)
        logger.info(f"Client {username} disconnected from WebSocket.")

        # Értesítsük a többi klienst a felhasználó kilépéséről
        await mh.handle_message("[SERVER]", f"{username} disconnected.")

async def start_ws_server(host, port):
    server = await websockets.serve(handle_client, host, port)
    logger.info(f"WebSocket server started on {host}:{port}")
    await server.wait_closed()