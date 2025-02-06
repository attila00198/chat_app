from logging_config import setup_logging

# Configure logging
logger = setup_logging('message_handler')

class MessageHandler:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    async def broadcast_message(self, username, message):
        """Üzenet küldése minden kliensnek, kivéve azt, aki küldte."""
        msg_to_send = f"{username}: {message}"
        for user in self.client_manager.get_all_users():
            if user != username:
                client_socket = self.client_manager.get_client_socket(user)
                try:
                    await client_socket.send(msg_to_send)
                except Exception as e:
                    logger.error(f"WebSocket hiba: {e}")