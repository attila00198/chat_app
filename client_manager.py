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
            logger.info(
                f"New user added: '{username}' from '{client_socket.remote_address[0]}'"
            )

    async def remove_client(self, username):
        async with self.lock:
            if username in self.connected_users:
                del self.connected_users[username]
                logger.info(f"User: '{username}' removed.")

    async def get_user_by_name(self, username):
        async with self.lock:
            if username in self.connected_users:
                return username, self.connected_users[username]
            return

    async def get_all_user(self):
        async with self.lock:
            return self.connected_users
