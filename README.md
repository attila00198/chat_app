# Chat Application

## Overview
This project is a simple chat application consisting of a server and client. The server handles multiple clients, broadcasting messages and handling commands. The client connects to the server, sends messages, and receives broadcasts.

## Project Structure
```
chat_app/
├── client.py
├── server.py
├── client_manager.py
├── command_manager.py
├── command_list.py
├── logging_config.py
├── config.ini
└── README.md
```

## Configuration
The `config.ini` file contains server configuration settings:
```ini
[server]
host = localhost
port = 6969
buffsize = 1024
```

## Server Components

1. **server.py**
   - Starts the server and listens for client connections.
   - Handles client connections and broadcasts messages.
   - Uses `client_manager` to manage connected clients.
   - Uses `command_manager` to handle commands.

2. **client_manager.py**
   - Manages the list of connected clients.
   - Adds and removes clients.
   - Provides methods to get client sockets and usernames.

3. **command_manager.py**
   - Manages commands that clients can use.
   - Registers and handles commands.
   - Uses `command_list` for predefined commands.

4. **command_list.py**
   - Contains predefined commands such as `list_users` and `whisper`.
   - Uses `client_manager` to interact with clients.

5. **logging_config.py**
   - Provides a centralized logging configuration.
   - Sets up logging for different modules.

## Usage

- **Starting the Server**
   - Run the server:
     ```sh
     python server.py
     ```

## Commands
- **/list_users**: Lists all currently connected users.
- **/whisper <username> <message>**: Sends a private message to a specific user.

## Logging
- Logs are configured using the `logging_config.py` module.
- Logs include timestamps, log levels, and messages.

## Example Log Entry
```
21-10-15 14:30 | INFO | Client connected from ('127.0.0.1', 12345)
```

This documentation provides a minimal overview of the project structure, configuration, components, usage, commands, and logging. For more detailed information, refer to the source code and comments within each file.
