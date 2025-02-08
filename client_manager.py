import json
import asyncio
from logging_config import setup_logging

# Configure logging
logger = setup_logging("client_manager")


class ClientManager:
    _instance = None
    lock = asyncio.Lock()
    connected_users = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClientManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.connected_users = {}
            logger.info("ClientManager initialized.")
        return cls._instance

    async def add_client(self, username, client_socket):
        async with self.lock:
            self.connected_users[username] = client_socket
            logger.info(f"User '{username}' added to connected users.")
            await self.send_user_list()

    async def remove_client(self, username):
        async with self.lock:
            if username in self.connected_users:
                del self.connected_users[username]
                logger.info(f"User '{username}' removed form connected users")
                await self.send_user_list()

    async def get_user_by_name(self, username):
        async with self.lock:
            if username in self.connected_users:
                return username, self.connected_users[username]
            return

    async def get_all_user(self):
        async with self.lock:
            return self.connected_users

    async def send_user_list(self):
        message_to_send = {
            "type": "user_list_update",
            "sender": "System",
            "content": list(self.connected_users.keys())
        }

        for client_socket in self.connected_users.values():
            await client_socket.send(json.dumps(message_to_send))
