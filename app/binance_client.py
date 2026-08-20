import asyncio
import json
import ssl
import certifi
import logging
from websockets.asyncio.client import connect
from app.connection_manager import ConnectionManager
from websockets.exceptions import ConnectionClosed
from app.symbols import SYMBOLS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

base_url = "wss://stream.binance.com:9443/stream?streams="
decorated_url_tag = "/".join([symbol.lower() + "@aggTrade" for symbol in SYMBOLS])
combined_stream = base_url + decorated_url_tag
ssl_context = ssl.create_default_context(cafile=certifi.where())

async def stream_trades(manager: ConnectionManager):
    async for websocket in connect(combined_stream, ssl=ssl_context):
        try:
            async for message in websocket:
                payload = json.loads(message)
                symbol = payload["data"]["s"]
                price = payload["data"]["p"]
                quantity = payload["data"]["q"]
                trade = { "symbol": symbol, "price": price, "quantity": quantity }

                await manager.broadcast(trade)
                # logging.info("%s price=%s qty=%s", symbol, price, quantity)
        except ConnectionClosed as e:
            logging.warning("Connection closed: %s", e)
            continue

async def stream_trades_infinite_run(manager: ConnectionManager):
    while True:
        try:
            await stream_trades(manager)
        except Exception as e:
            logging.error("An error occured %s", e)
        await asyncio.sleep(2)

if __name__ == "__main__":
    manager = ConnectionManager(SYMBOLS)
    asyncio.run(stream_trades_infinite_run(manager))