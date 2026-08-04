from unittest.mock import AsyncMock
from app.connection_manager import ConnectionManager

async def test_connect_accepts_and_adds_to_active_connections():
    connection_manager = ConnectionManager({"BTCUSDT"})
    fake_websocket = AsyncMock()
    await connection_manager.connect(fake_websocket)
    fake_websocket.accept.assert_called_once()
    assert fake_websocket in connection_manager.active_connections

async def test_disconnect_removes_from_active_connections():
    connection_manager = ConnectionManager({"BTCUSDT"})
    fake_websocket = AsyncMock()
    await connection_manager.connect(fake_websocket)
    assert fake_websocket in connection_manager.active_connections
    connection_manager.disconnect(fake_websocket)
    assert fake_websocket not in connection_manager.active_connections

async def test_broadcast_sends_to_all_connections():
    connection_manager = ConnectionManager({"BNBUSDT"})
    fake_websocket_a = AsyncMock()
    fake_websocket_b = AsyncMock()
    message = { "symbol": "BNBUSDT", "price": 21899.02, "quantity": 0.5348 }
    await connection_manager.connect(fake_websocket_a)
    await connection_manager.connect(fake_websocket_b)
    await connection_manager.broadcast(message)
    fake_websocket_a.send_json.assert_called_with(message)
    fake_websocket_b.send_json.assert_called_with(message)

async def test_broadcast_removes_only_the_failing_connection():
    connection_manager = ConnectionManager({"AVAXUSDT"})
    fake_websocket_good = AsyncMock()
    fake_websocket_bad = AsyncMock()
    fake_websocket_bad.send_json.side_effect = Exception("dead")
    message = { "symbol": "AVAXUSDT", "price": 22897.35, "quantity": 0.2738 }
    await connection_manager.connect(fake_websocket_good)
    await connection_manager.connect(fake_websocket_bad)
    await connection_manager.broadcast(message)
    assert fake_websocket_good in connection_manager.active_connections
    assert fake_websocket_bad not in connection_manager.active_connections
    fake_websocket_good.send_json.assert_called_with(message)