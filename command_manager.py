from threading import Lock
from command_list import list_users, whisper
from logging_config import setup_logging

# Configure logging
logger = setup_logging('command_manager')

class CommandManager:
    def __init__(self):
        self.commands = {}
        self.lock = Lock()
        logger.info("CommandManager initialized.")
        self.register_command("/list", list_users)
        self.register_command("/whisper", whisper)

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