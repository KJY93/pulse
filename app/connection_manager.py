import asyncio

from fastapi import WebSocket

class ConnectionManager:

    def __init__(self, default_symbols):
        self.default_symbols = default_symbols
        self.active_connections: dict[WebSocket, set[str]] = dict()

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.update({ websocket: set(self.default_symbols) })

    def disconnect(self, websocket):
        self.active_connections.pop(websocket, None)

    async def broadcast(self, message: dict):
        fail_connections: set[WebSocket] = set()
        connections = [ws for ws, sub in self.active_connections.items() if message["symbol"] in sub]

        tasks = [asyncio.wait_for(conn.send_json(message), timeout=500) for conn in connections]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for connection, result in zip(connections, results):
            if isinstance(result, Exception):
                fail_connections.add(connection)
            
        for fail_connection in fail_connections:
            self.disconnect(fail_connection)

    def update_subscription(self, websocket, symbols):
        self.active_connections[websocket] = set(symbols)