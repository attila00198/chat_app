from command_manager import command_manager
from logging_config import setup_logging

# Configure logging
logger = setup_logging('message_handler')

class MessageHandler:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    async def handle_message(self, username, message):
        if message.startswith("/"):
            # Handle command if the message is a command
            await command_manager.handle_command(username, message)
        else:
            # Broadcast regular message to other users
            await self.broadcast_message(username, message)

    async def broadcast_message(self, username, message):
        """Üzenet küldése minden kliensnek, kivéve azt, aki küldte."""
        msg_to_send = f"{username}: {message}"
        for user in self.client_manager.get_all_users():
            if user != username:
                await self.send_message_to_user(user, msg_to_send)

    async def send_message_to_user(self, user, message):
        """Üzenet küldése a megfelelő kliens típusnak (TCP vagy WebSocket)."""
        client_socket = self.client_manager.get_client_socket(user)
        client_type = self.client_manager.get_client_type(user)

        if client_socket:
            if client_type == 'websocket':
                await self.send_websocket_message(client_socket, message)
            elif client_type == 'tcp':
                await self.send_tcp_message(client_socket, message)

    async def send_websocket_message(self, client_socket, message):
        """Üzenet küldése WebSocket kliensnek."""
        try:
            await client_socket.send(message)
        except Exception as e:
            logger.error(f"WebSocket hiba: {e}")

    async def send_tcp_message(self, client_socket, message):
        """Üzenet küldése TCP kliensnek."""
        try:
            client_socket.write(message.encode())
            await client_socket.drain()
        except Exception as e:
            logger.error(f"TCP hiba: {e}")