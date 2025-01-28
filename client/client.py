import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "!NICKNAME":
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()
            break

if __name__ == "__main__":
    nickname = input("Choose your nickname: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 6969))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        exit()

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receive_thread.start()

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