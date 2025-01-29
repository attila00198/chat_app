from logging_config import setup_logging
import threading

# Configure logging
logger = setup_logging('client_manager')

class ClientManager:
    def __init__(self):
        self.client_list = {}
        self.lock = threading.Lock()
        logger.info("ClientManager initialized.")

    def add_client(self, username, client_socket, client_type):
        with self.lock:
            self.client_list[username] = (client_socket, client_type)
            logger.info(f"Client {username} added as {client_type}.")

    def remove_client(self, username):
        with self.lock:
            if username in self.client_list:
                del self.client_list[username]
                logger.info(f"Client {username} removed.")

    def get_client_socket(self, username):
        with self.lock:
            client_info = self.client_list.get(username)
            return client_info[0] if client_info else None

    def get_client_type(self, username):
        with self.lock:
            client_info = self.client_list.get(username)
            return client_info[1] if client_info else None

    def get_all_users(self):
        with self.lock:
            return list(self.client_list.keys())

    def get_username(self, client_socket):
        with self.lock:
            for username, (socket, _) in self.client_list.items():
                if socket == client_socket:
                    return username
            return None

client_manager = ClientManager()