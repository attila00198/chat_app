import asyncio
from client_manager import client_manager
from message_handler import handle_message
from logging_config import setup_logging

# Configure logging
logger = setup_logging('tcp_server')

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logger.info(f"Accepted connection from {addr}")

    # Kérjük a felhasználónevet
    writer.write("!NICKNAME".encode())
    await writer.drain()

    try:
        username = await reader.read(1024)
        username = username.decode()
        client_manager.add_client(username, writer, 'tcp')
        logger.info(f"Client {username} connected.")

        # Értesítsük a többi klienst az új felhasználó csatlakozásáról
        await handle_message("[SERVER]", f"{username} connected.")

        while True:
            data = await reader.read(1024)
            message = data.decode()
            if not message:
                break
            await handle_message(username, message)
    except ConnectionResetError:
        logger.warning(f"Connection reset by {username}")
    finally:
        client_manager.remove_client(username)
        writer.close()
        await writer.wait_closed()
        logger.info(f"Client {username} disconnected.")

        # Értesítsük a többi klienst a felhasználó kilépéséről
        await handle_message("[SERVER]", f"{username} disconnected.")

async def start_tcp_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    logger.info(f"TCP server started on {host}:{port}")
    async with server:
        await server.serve_forever()