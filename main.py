from app.connection_manager import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from app.binance_client import stream_trades
import asyncio
from app.symbols import SYMBOLS


manager = ConnectionManager(SYMBOLS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(stream_trades(manager))
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)