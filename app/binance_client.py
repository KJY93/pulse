import asyncio
import json
import ssl
import certifi
import logging
from websockets.asyncio.client import connect

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

async def stream_trades():
    async with connect(combined_stream, ssl=ssl_context) as websocket:
        logging.info("a websocket connection has been established.")

        async for message in websocket:
            payload = json.loads(message)
            symbol = payload["data"]["s"]
            price = payload["data"]["p"]
            quantity = payload["data"]["q"]

            logging.info("%s price=%s qty=%s", symbol, price, quantity)

if __name__ == "__main__":
    asyncio.run(stream_trades())