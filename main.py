from app.connection_manager import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)