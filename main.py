import asyncio
import configparser
from tcp_server import start_tcp_server
from ws_server import start_ws_server

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')
tcp_host = config['tcp_server']['host']
tcp_port = int(config['tcp_server']['port'])
ws_host = config['ws_server']['host']
ws_port = int(config['ws_server']['port'])

async def main():
    tcp_task = asyncio.create_task(start_tcp_server(tcp_host, tcp_port))
    ws_task = asyncio.create_task(start_ws_server(ws_host, ws_port))

    await asyncio.gather(tcp_task, ws_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server is shutting down...")