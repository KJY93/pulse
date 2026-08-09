from app.connection_manager import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from app.binance_client import stream_trades_infinite_run
import asyncio
import json
from app.symbols import SYMBOLS


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
            subcription_payload = json.loads(await websocket.receive_text())
            symbols = subcription_payload["symbols"]
            manager.update_subscription(websocket, symbols)
    except WebSocketDisconnect:
        manager.disconnect(websocket)