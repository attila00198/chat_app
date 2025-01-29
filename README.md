# Chat Application

## Overview
This project is a simple chat application consisting of a server and client. The server handles multiple clients, broadcasting messages and handling commands. The client connects to the server, sends messages, and receives broadcasts.

## Project Structure
```
chat_app/
├── client.py
├── tcp_server.py
├── ws_server.py
├── client_manager.py
├── command_manager.py
├── command_list.py
├── message_handler.py
├── logging_config.py
├── config.ini
└── README.md
```

## Configuration
The `config.ini` file contains server configuration settings:
```ini
[tcp_server]
host = localhost
port = 6969

[ws_server]
host = localhost
port = 6968
```

## Server Components

1. **tcp_server.py**
   - Starts the TCP server and listens for client connections.
   - Handles client connections and broadcasts messages.
   - Uses `client_manager` to manage connected clients.
   - Uses `command_manager` to handle commands.

2. **ws_server.py**
   - Starts the WebSocket server and listens for client connections.
   - Handles client connections and broadcasts messages.
   - Uses `client_manager` to manage connected clients.
   - Uses `command_manager` to handle commands.

3. **client_manager.py**
   - Manages the list of connected clients.
   - Adds and removes clients.
   - Provides methods to get client sockets and usernames.

4. **command_manager.py**
   - Manages commands that clients can use.
   - Registers and handles commands.
   - Uses `command_list` for predefined commands.

5. **command_list.py**
   - Contains predefined commands such as `list_users` and `whisper`.
   - Uses `client_manager` to interact with clients.

6. **message_handler.py**
   - Handles incoming messages and broadcasts them to clients.
   - Uses `command_manager` to handle commands.

7. **logging_config.py**
   - Provides a centralized logging configuration.
   - Sets up logging for different modules.

## Client Component

1. **client.py**
   - Connects to the TCP server.
   - Sends and receives messages.
   - Handles user input and server responses.

## Usage

1. **Starting the TCP Server**
   - Run the server:
     ```sh
     python tcp_server.py
     ```

2. **Starting the WebSocket Server**
   - Run the WebSocket server:
     ```sh
     python ws_server.py
     ```

3. **Starting the Client**
   - Run the client:
     ```sh
     python client.py
     ```
   - Enter a nickname when prompted.
   - Type messages to send to the server.
   - Use `!quit` to disconnect from the server.

## Commands
- **/list**: Lists all currently connected users.
- **/whisper <username> <message>**: Sends a private message to a specific user.

## Logging
- Logs are configured using the `logging_config.py` module.
- Logs include timestamps, log levels, and messages.

## Example Log Entry
```
21-10-15 14:30 | INFO | Client connected from ('127.0.0.1', 12345)
```

This documentation provides a minimal overview of the project structure, configuration, components, usage, commands, and logging. For more detailed information, refer to the source code and comments within each file.
