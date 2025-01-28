import threading
from logging_config import setup_logging

# Configure logging
logger = setup_logging('client_manager')

class ClientManager:
    def __init__(self):
        self.client_list = {}
        self.lock = threading.Lock()
        logger.info("ClientManager initialized.")

    def add_client(self, username, client_socket):
        with self.lock:
            if username in self.client_list:
                client_socket.send("Username already taken. Please reconnect with a different name.".encode())
                client_socket.close()
                logger.warning(f"Username {username} already taken.")
            else:
                self.client_list[username] = client_socket
                logger.info(f"Added client {username}")

    def remove_client(self, username):
        with self.lock:
            if username in self.client_list:
                del self.client_list[username]
                logger.info(f"Removed client {username}")

    def get_client_socket(self, username):
        with self.lock:
            return self.client_list.get(username)

    def get_all_users(self):
        with self.lock:
            return list(self.client_list.keys())

    def get_username(self, client_socket):
        with self.lock:
            for username, sock in self.client_list.items():
                if sock == client_socket:
                    return username
            return None

client_manager = ClientManager()