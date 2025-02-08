import json
import logging
from pydantic import BaseModel
from typing import List, Optional
from client_manager import ClientManager
from command_manager import CommandManager

# Logging beállítás
logger = logging.getLogger("message_handler")


# Pydantic model az üzenetekhez
class Message(BaseModel):
    type: str
    sender: str
    content: str
    target: Optional[List[str]] = None  # Opcionális címzettlista


class MessageHandler:
    def __init__(self):
        self.command_manager = CommandManager()
        self.client_manager = ClientManager()

    async def handle_message(self, message: Message):
        """Az üzenet megfelelő handlerhez továbbítása."""
        if message.type == "message":
            await self.handle_chat_message(message)
        elif message.type == "command":
            await self.handle_command(message)

    async def handle_chat_message(self, message: Message):
        """Chat üzenetek továbbítása."""
        await self.broadcast_message(message.sender, message.content, message.target)

    async def handle_command(self, message: Message):
        """Parancsok kezelése."""
        await self.command_manager.handle_command(message.sender, message.content)

    async def broadcast_message(
        self, sender: str, message: str, target: Optional[List[str]] = None
    ):
        """Üzenet küldése minden kliensnek, vagy csak a megadott címzetteknek."""
        message_data = json.dumps(
            {"type": "message", "sender": sender, "content": message, "target": target}
        )

        user_dict = await self.client_manager.get_all_user()

        # Ha van target, akkor csak nekik küldjük el az üzenetet
        recipients = (
            user_dict
            if target is None
            else {user: user_dict[user] for user in target if user in user_dict}
        )

        for user, client_socket in recipients.items():
            if user != sender:
                try:
                    await client_socket.send(message_data)
                except Exception as e:
                    logger.error(f"WebSocket error: {e}")
