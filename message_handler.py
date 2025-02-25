from logging_config import setup_logging
from client_manager import ClientManager
from command_manager import CommandManager
from models import Message


class MessageHandler:
    """Class for handling messages"""

    def __init__(self):
        """
        Inicializing the MessageHandler.
        """
        self.logger = setup_logging("MessageHandler")
        self.logger.info("MessageHandler initialized.")

        # Initializing components
        self.command_manager = CommandManager()
        self.client_manager = ClientManager()

        # Üzenettípusok és kezelőik összerendelése
        self.message_handlers = {
            "message": self.handle_chat_message,  # Simple chat messages. Thay can be sent by users or tha system
            "command": self.handle_command,  # Commands
            # Temporary solution for system and error messages
            "system": self.handle_chat_message,
            "error": self.handle_chat_message,
            # TODO Add more message types if needed (e.g. group messages, private messages)
            # "private_message": self.send_private_message,
            # "group_message": self.send_group_message,
        }

    async def dispatch_message(self, message: Message) -> None:
        """
        Handling messages based on their type.

        Args:
            message: message to process

        Raises:
            ValueError: if the message type is unknown
        """
        try:
            handler = self.message_handlers.get(message.type)
            if handler:
                await handler(message)
            else:
                raise ValueError(f"Unknown message type: {message.type}")
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            raise

    async def handle_chat_message(self, message: Message) -> None:
        """
        Handling chat, system and error messages.

        Args:
            message: Message to relay
        """
        try:
            await self.broadcast_message(message)
        except Exception as e:
            self.logger.error(f"Error handling chat message: {e}")
            raise

    async def handle_command(self, message: Message) -> None:
        """
        Passing the command to the command manager.

        Args:
            message: A végrehajtandó parancs
        """
        try:
            await self.command_manager.execute_command(
                sender=message.sender, message=message.content
            )
        except Exception as e:
            self.logger.error(f"Error handling command: {e}")
            raise

    async def send_private_message(self, target: str, message=Message) -> None:
        """
        Sending private message to the target.

        Args:
            message: Message object
            target: Recipient's identifier/nickname
        """
        try:
            message = Message(
                type=message.type, sender=message.sender, content=message.content
            ).model_dump_json()

            user_dict = await self.client_manager.get_all_user()
            recipient = self._get_recipients(user_dict, [target])

            for _, client_socket in recipient.items():
                try:
                    await client_socket.send(message)
                except Exception as e:
                    self.logger.error(f"Error sending private message: {e}")
                    raise

        except Exception as e:
            self.logger.error(f"Error sending private message: {e}")
            raise

    async def broadcast_message(
        self,
        message: Message,
    ) -> None:
        """
        Sending message to all users.

        Args:
            sender: sender's identifier/nickname
            content: message content
        """

        message_to_send = message.model_dump_json()
        all_users = await self.client_manager.get_all_user()

        try:
            for user, client_socket in all_users.items():
                try:
                    if user != message.sender:
                        await client_socket.send(message_to_send)
                except Exception as e:
                    self.logger.error(f"Error sending to {user}: {e}")

        except Exception as e:
            self.logger.error(f"Error while trying to send message: {e}")
            raise

    async def send_user_list(self):
        all_users = await self.client_manager.get_all_user()
        message_to_send = Message(
            type="user_list_update",
            sender="System",
            content=list(all_users.keys()),
        ).model_dump_json()

        for user, client_socket in all_users.items():
            try:
                await client_socket.send(message_to_send)
            except Exception as e:
                self.logger.error(f"Error sending user list to {user}: {e}")
                raise
