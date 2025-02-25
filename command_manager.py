from asyncio import Lock
from logging_config import setup_logging
from client_manager import ClientManager
from models import Message

# Configure logging
logger = setup_logging("CommandManager")


class CommandManager:
    """
    Class for managing commands.
    """

    def __init__(self):
        self.commands = {}
        self.client_manager = ClientManager()
        self.lock = Lock()

        logger.info("CommandManager initialized.")

        self.register_commands()

    def command(
        self, name: str = None, aliases: list[str] = None, description: str = None
    ):
        """Decorator for registering a new command.

        Args:
            name (str): The name of the command. Defaults to the function name.
            aliases (list): A list of aliases for the command.
            description (str): A description of the command.
        """

        def decorator(func):
            cmd_name = name or func.__name__
            command_info = {
                "handler": func,
                "aliases": aliases or [],
                "description": description or func.__doc__ or "Nincs leírás",
            }
            self.commands[cmd_name] = command_info
            for alias in command_info["aliases"]:
                self.commands[alias] = command_info
            return func

        return decorator

    def register_commands(self):
        """
        Registers a command with a given name and handler function.
        """

        @self.command(
            name="help", aliases=["h", "?"], description="List all available commands"
        )
        async def help(self, sender: str, args: list[str]=None):
            """List all available commands"""
            commands_list = "Elérhető parancsok:\n"
            unique_commands = {}

            for cmd_name, cmd_info in self.commands.items():
                # filter out aliases
                if cmd_name not in [
                    alias
                    for c_info in self.commands.values()
                    for alias in c_info.get("aliases", [])
                ]:
                    unique_commands[cmd_name] = cmd_info

            for cmd_name, cmd_info in unique_commands.items():
                aliases = ", ".join(cmd_info["aliases"])
                if aliases:
                    commands_list += (
                        f"/{cmd_name} (Aliases: {aliases}) - {cmd_info['description']}\n"
                    )
                else:
                    commands_list += f"/{cmd_name} - {cmd_info['description']}\n"

            user_to_send = await self.client_manager.get_user_by_name(sender)
            msg_to_send = Message(
                sender="System",
                type="info",
                target=sender,
                content=commands_list,
            ).model_dump_json()
            _, client_socket = user_to_send
            await client_socket.send(msg_to_send)

    async def execute_command(self, sender: str, message: str):
        """
        Handles the command sent by the user.

        Args:
            sender: The user of the command
            command: The command to be executed
        """

        try:
            cmd, *args = message.strip("/").split(maxsplit=1)
            logger.debug(f"Command received: {cmd}")
            logger.debug(f"Args received: {args}")

            user_to_send = await self.client_manager.get_user_by_name(sender)
            msg_to_send = Message(
                sender="System",
                type="error",
                target=sender,
                content=f"Command '{cmd}' not found.",
            ).model_dump_json()

            if cmd in self.commands:
                await self.commands[cmd]["handler"](self, sender, args)
            else:
                _, client_socket = user_to_send
                await client_socket.send(msg_to_send)
                logger.error(f"Command '{cmd}' not found.")
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            raise
