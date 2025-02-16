import json
from client_manager import ClientManager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('command_list')
client_manager = ClientManager()

async def list_users(username, args=None):
    """
    Lists all currently connected users.
    """
    users = await client_manager.get_all_user()
    if not users:
        logger.info("No users connected.")
        return

    user_to_send = await client_manager.get_user_by_name(username)
    if not user_to_send:
        logger.error("An error ocured wnile searching for user to send")
        return

    _, socket = user_to_send
    message_to_send = {
        "type": "message",
        "sender": "System",
        "content": "Currently online user(s):\n" + "\n".join(users.keys())
    }
    await socket.send(json.dumps(message_to_send))
