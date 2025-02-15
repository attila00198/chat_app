import asyncio
import configparser
from ws_server import start_ws_server

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')

ws_host = config['ws_server']['host']
ws_port = int(config['ws_server']['port'])


async def main():
    ws_task = asyncio.create_task(start_ws_server(ws_host, ws_port))

    await asyncio.gather(ws_task)

if __name__ == "__main__":
    try:
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        print("Server is shutting down...")
