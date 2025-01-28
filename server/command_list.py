from client_manager import client_manager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('command_list')

def list_users(client, args=None):
    users = list(client_manager.client_list.keys())
    client.send(f"Currently online: {', '.join(users)}".encode())
    logger.info("Listed users")

def whisper(client, args=None):
    if not args or len(args.split(" ", 1)) < 2:
        client.send("Usage: /whisper <username> <message>".encode())
        logger.warning("Whisper command used incorrectly")
        return

    target_name, message = args.split(" ", 1)
    send_to = client_manager.get_client_socket(target_name)
    if send_to:
        send_to.send(f"[Whisper] {client_manager.get_username(client)}: {message}".encode())
        logger.info(f"Whispered to {target_name}")
    else:
        client.send(f"User {target_name} not found.".encode())
        logger.warning(f"User {target_name} not found")