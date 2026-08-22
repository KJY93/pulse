from app.connection_manager import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from app.binance_client import stream_trades_infinite_run
import asyncio
from app.rate_limiter import is_rate_limited
from app.symbols import SYMBOLS
from app.subscribe_parser import parse_subscribe_message

manager = ConnectionManager(SYMBOLS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(stream_trades_infinite_run(manager))
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            raw_text = await websocket.receive_text()
            client_ip = websocket.client.host

            if is_rate_limited(client_ip, limit=10, window_seconds=1):
                await websocket.send_json({"error": "rate limited", "message": "Too many requests"})
                continue
            
            symbols = parse_subscribe_message(raw_text)

            if symbols is not None:
                manager.update_subscription(websocket, symbols)
    except WebSocketDisconnect:
        manager.disconnect(websocket)