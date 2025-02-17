import json
from typing import List, Optional, Dict
from pydantic import BaseModel
from websockets import WebSocketServerProtocol
from logging_config import setup_logging
from client_manager import ClientManager
from command_manager import CommandManager

class Message(BaseModel):
    """Üzenetek validálására szolgáló Pydantic model"""
    type: str
    sender: str
    content: str
    target: Optional[List[str]] = None


class MessageHandler:
    """Üzenetek kezelésére szolgáló osztály"""

    def __init__(self,):
        """
        MessageHandler inicializálása.

        Args:
            logger_name: A logger neve
        """
        self.logger = setup_logging("MessageHandler")
        self.command_manager = CommandManager()
        self.client_manager = ClientManager()

        # Üzenettípusok és kezelőik összerendelése
        self.message_handlers = {
            "message": self.handle_chat_message,
            "command": self.handle_command
        }

    async def handle_message(self, message: Message) -> None:
        """
        Üzenet továbbítása a megfelelő kezelőhöz.

        Args:
            message: A feldolgozandó üzenet

        Raises:
            ValueError: Ha ismeretlen üzenettípust kap
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
        Chat üzenetek kezelése.

        Args:
            message: A továbbítandó chat üzenet
        """
        try:
            await self.broadcast_message(
                sender=message.sender,
                content=message.content,
                target=message.target
            )
        except Exception as e:
            self.logger.error(f"Error handling chat message: {e}")
            raise

    async def handle_command(self, message: Message) -> None:
        """
        Parancsok kezelése.

        Args:
            message: A végrehajtandó parancs
        """
        try:
            await self.command_manager.handle_command(
                message.sender,
                message.content
            )
        except Exception as e:
            self.logger.error(f"Error handling command: {e}")
            raise

    async def broadcast_message(
        self,
        sender: str,
        content: str,
        target: Optional[List[str]] = None
    ) -> None:
        """
        Üzenet küldése a megadott címzetteknek vagy minden kliensnek.

        Args:
            sender: Küldő azonosítója
            content: Az üzenet tartalma
            target: Opcionális címzettlista
        """
        try:
            message_data = json.dumps({
                "type": "message",
                "sender": sender,
                "content": content,
                "target": target
            })

            # Címzettek meghatározása
            user_dict = await self.client_manager.get_all_user()
            recipients = self._get_recipients(user_dict, target)

            # Üzenet küldése
            await self._send_to_recipients(
                message_data=message_data,
                recipients=recipients,
                sender=sender
            )

        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")
            raise

    def _get_recipients(
        self,
        user_dict: Dict[str, WebSocketServerProtocol],
        target: Optional[List[str]]
    ) -> Dict[str, WebSocketServerProtocol]:
        """
        Címzettek szűrése a target lista alapján.

        Args:
            user_dict: Az összes felhasználó szótára
            target: Opcionális címzettlista

        Returns:
            A szűrt címzettek szótára
        """
        if target is None:
            return user_dict
        return {
            user: socket
            for user, socket in user_dict.items()
            if user in target
        }

    async def _send_to_recipients(
        self,
        message_data: str,
        recipients: Dict[str, WebSocketServerProtocol],
        sender: str
    ) -> None:
        """
        Üzenet küldése a címzetteknek.

        Args:
            message_data: A küldendő üzenet JSON formátumban
            recipients: A címzettek szótára
            sender: A küldő azonosítója
        """
        for user, client_socket in recipients.items():
            if user != sender:
                try:
                    await client_socket.send(message_data)
                except Exception as e:
                    self.logger.error(f"Error sending to {user}: {e}")
