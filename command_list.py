from client_manager import client_manager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('command_list')

async def list_users(username, args=None):
    """
    Lists all currently connected users.
    """
    users = list(client_manager.get_all_users())
    if not users:
        logger.info("No users connected.")
        return
    send_to = client_manager.get_client_socket(username)
    client_type = client_manager.get_client_type(username)
    if client_type == 'websocket':
        await send_to.send(f"Connected users: {', '.join(users)}")
    else:
        send_to.write(f"Connected users: {', '.join(users)}".encode())
        await send_to.drain()
    logger.info(f"Command /list used by {username}")

async def whisper(username, args):
    """
    Sends a private message to a specific user.
    """
    sender_socket = client_manager.get_client_socket(username)
    sender_type = client_manager.get_client_type(username)
    
    if not args:
        if sender_type == 'websocket':
            await sender_socket.send("Usage: /whisper <username> <message>")
        else:
            sender_socket.write("Usage: /whisper <username> <message>".encode())
            await sender_socket.drain()
        return
    
    parts = args.split(" ", 1)
    recipient = parts[0]
    message = parts[1] if len(parts) > 1 else None
    if not message:
        return

    recipient_socket = client_manager.get_client_socket(recipient)
    if recipient_socket:
        recepient_type = client_manager.get_client_type(recipient)
        if recepient_type == 'websocket':
            await recipient_socket.send(f"[WHISPER] {username}: {message}")
        else:
            recipient_socket.write(f"[WHISPER] {username}: {message}".encode())
    else:
        if sender_type == 'websocket':
            sender_socket.send(f"User {recipient} not found.")
        else:
            sender_socket.write(f"User {recipient} not found.".encode())