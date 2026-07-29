import asyncio
import json
import ssl
import certifi
import logging
from websockets.asyncio.client import connect
from app.connection_manager import ConnectionManager
from websockets.exceptions import ConnectionClosed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

SYMBOLS = [
    "btcusdt", "ethusdt", "bnbusdt", "solusdt", "xrpusdt",
    "adausdt", "dogeusdt", "avaxusdt", "dotusdt", "linkusdt"
]

base_url = "wss://stream.binance.com:9443/stream?streams="
decorated_url_tag = "/".join([symbol + "@aggTrade" for symbol in SYMBOLS])
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
                logging.info("%s price=%s qty=%s", symbol, price, quantity)
        except ConnectionClosed as e:
            logging.warning("Connection closed: %s", e)
            continue


if __name__ == "__main__":
    manager = ConnectionManager()
    asyncio.run(stream_trades(manager))