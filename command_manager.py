import json
from threading import Lock
from logging_config import setup_logging
from client_manager import ClientManager
from command_list import list_users

# Configure logging
logger = setup_logging("CommandManager")


class CommandManager:
    def __init__(self):
        self.commands = {}
        self.client_manager = ClientManager()
        self.lock = Lock()
        logger.info("CommandManager initialized.")
        self.register_command("/listUsers", list_users)

    def register_command(self, name, func):
        """
        Registers a command with the given name and function.
        """
        with self.lock:
            self.commands[name] = func

    async def handle_command(self, username, message):
        """
        Handles a command sent by a client.
        """
        parts = message.split(" ", 1)
        command_name = parts[0]
        args = parts[1] if len(parts) > 1 else None
        if command_name in self.commands:
            await self.commands[command_name](username, args)
        else:
            user = await self.client_manager.get_user_by_name(username)
            if user:
                _, socket = user
                msg = {
                    "type": "message",
                    "sender": "System",
                    "content": f"Command not Found {command_name}"
                }
                await socket.send(json.dumps(msg))
