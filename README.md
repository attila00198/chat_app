# Chat Application

This is a simple chat application that supports both WebSocket and TCP connections. It allows users to send messages to each other and execute commands.

## Features

- Supports WebSocket and TCP connections
- Broadcast messages to all connected clients
- Handle commands such as listing users and sending private messages

## Setup

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd chat_app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure the server settings in `config.ini`:
    ```ini
    [tcp_server]
    host = localhost
    port = 6969

    [ws_server]
    host = localhost
    port = 6968
    ```

## Project Structure
```
chat_app/
├── main.py
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

1. **main.py**
   - Starts the TCP and WebSocket servers.

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


## Usage

1. **Starting the Server**
   - Run the server:
     ```sh
     python main.py
     ```

## Available Commands
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
