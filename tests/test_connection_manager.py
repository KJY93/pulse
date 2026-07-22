import pytest
from unittest.mock import AsyncMock
from app.connection_manager import ConnectionManager

async def test_connect_accepts_and_adds_to_active_connections():
    connection_manager = ConnectionManager()
    fake_websocket = AsyncMock()
    await connection_manager.connect(fake_websocket)
    fake_websocket.accept.assert_called_once()
    assert fake_websocket in connection_manager.active_connections