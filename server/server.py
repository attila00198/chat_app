import configparser
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, Lock
from client_manager import client_manager
from command_manager import command_manager
from logging_config import setup_logging

# Setup logging
logger = setup_logging('server')

# Verify logging configuration
logger.info("Logging is configured correctly.")

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
HOST = config.get('server', 'host', fallback='localhost')
PORT = config.getint('server', 'port', fallback=6969)
BUFFSIZE = config.getint('server', 'buffsize', fallback=1024)

lock = Lock()


def broadcast(message, sender=None):
    full_msg = f"{sender}: {message}" if sender else f"[SERVER]: {message}"
    to_remove = []

    for username, client_socket in client_manager.client_list.items():
        try:
            if username != sender:
                client_socket.send(full_msg.encode())
        except Exception as e:
            logger.error(f"Error sending message to {username}: {e}")
            to_remove.append(username)
    with lock:
        for username in to_remove:
            client_manager.remove_client(username)


def handle_client(client_socket, address):
    logger.info(f"Client connected from {address}")

    client_socket.send("!NICKNAME".encode())
    username = client_socket.recv(BUFFSIZE).decode().strip()
    client_manager.add_client(username, client_socket)

    broadcast(f"{username} connected.")
    try:
        while True:
            message = client_socket.recv(BUFFSIZE).decode()
            if not message:
                break
            else:
                if message[0] == "/":
                    command_manager.handle_command(client_socket, message[1:])
                else:
                    broadcast(message, username)
    except Exception as e:
        logger.error(f"[Error]: {address}: {e}")
    finally:
        with lock:
            client_manager.remove_client(username)
        client_socket.close()
        broadcast(f"[SERVER]: {username} left the server.")
        logger.info(f"Client {address} disconnected")


if __name__ == "__main__":
    logger.info("Starting server...")
    ADDR = (HOST, PORT)
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SERVER.bind(ADDR)
    SERVER.listen(5)
    logger.info(f"Server is listening on {ADDR}...")

    try:
        while True:
            client_socket, address = SERVER.accept()
            client_thread = Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        logger.info("Server is shutting down...")
    finally:
        SERVER.close()
