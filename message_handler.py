from client_manager import client_manager
from command_manager import command_manager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('message_handler')

async def handle_message(username, message):
    if message.startswith("/"):
        await command_manager.handle_command(username, message)
        return
    msg_to_send = f"{username}: {message}"
    # Broadcast üzenet minden kliensnek
    for user in client_manager.get_all_users():
        if user != username:
            client_socket = client_manager.get_client_socket(user)
            client_type = client_manager.get_client_type(user)
            if client_socket:
                if client_type == 'websocket':
                    await client_socket.send(msg_to_send)
                elif client_type == 'tcp':
                    client_socket.write(msg_to_send.encode())
                    await client_socket.drain()