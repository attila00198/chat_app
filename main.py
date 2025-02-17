import asyncio
import configparser
import signal
from logging_config import setup_logging
from ws_server import WebSocketServer

logger = setup_logging("main")

config = configparser.ConfigParser()
config.read('config.ini')
ws_host = config['ws_server']['host']
ws_port = int(config['ws_server']['port'])


async def main():
    # WebSocketServer példányosítása
    ws_server = WebSocketServer('config.ini')

    # Graceful shutdown kezelése
    stop = asyncio.Event()

    def signal_handler():
        logger.info("Shutdown signal received...")
        stop.set()

    # Signal handlerek regisztrálása
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    # Szerver indítása
    ws_task = asyncio.create_task(ws_server.start(ws_host, ws_port))

    try:
        await stop.wait()  # Várunk a leállítási jelzésre
        ws_task.cancel()   # Task megszakítása
        await ws_task      # Megvárjuk a task leállását
    except asyncio.CancelledError:
        logger.info("WebSocket server task cancelled")
    finally:
        logger.info("Server shutdown complete")

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
