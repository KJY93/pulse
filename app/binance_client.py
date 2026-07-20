import asyncio
import json
import websockets

SYMBOLS = [
    "btcusdt", "ethusdt", "bnbusdt", "solusdt", "xrpusdt",
    "adausdt", "dogeusdt", "avaxusdt", "dotusdt", "linkusdt"
]

base_url = "wss://stream.binance.com:9443/stream?streams="

modified_url_tag = "/".join([symbol + "@aggTrade" for symbol in SYMBOLS])

combined_stream = base_url + modified_url_tag