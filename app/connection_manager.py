import asyncio

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
        connections = list(self.active_connections)

        tasks = [asyncio.wait_for(conn.send_json(message), timeout=500) for conn in connections]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for connection, result in zip(connections, results):
            if isinstance(result, Exception):
                fail_connections.add(connection)
            
        for fail_connection in fail_connections:
            self.disconnect(fail_connection)

