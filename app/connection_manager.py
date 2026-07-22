from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        fail_connections: set[WebSocket] = set()


        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                fail_connections.add(connection)

        for fail_connection in fail_connections:
            self.disconnect(fail_connection)

