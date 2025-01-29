import socket
import threading


def connect_to_server(host, port):
    """
    Connects to the server and returns the client socket.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        exit()
    return client_socket
    

def receive_messages(client_socket, nickname):
    """
    Receives messages from the server and prints them.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Server closed the connection.")
                client_socket.close()
                exit()
            if message == "!NICKNAME":
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()
            break

def send_message(client_socket):
    while True:
        try:
            message = input()
            if message == "!quit":
                print("Closing connection...")
                client_socket.close()
                break
            else:
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()
            break
        except KeyboardInterrupt:
            print("Closing connection...")
            client_socket.close()
            break

def main():
    try:
        HOST = input("Enter the server IP address: ") or "localhost"
        PORT = int(input("Enter the server port: ") or 6969)
        NICKNAME = input("Enter your nickname: ") or "Anonymous"

        client_socket = connect_to_server(HOST, PORT)

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, NICKNAME))
        receive_thread.daemon = True

        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        send_thread.daemon = True

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except Exception as e:
        print(f"An error occurred in the main function: {e}")
    finally:
        print("Client is shutting down...")

if __name__ == "__main__":
    main()