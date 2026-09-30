# Pulse

A real-time cryptocurrency trade dashboard. Live trades from Binance flow through a Python backend and out to connected browsers over a websocket, where each browser subscribes to just the coins it cares about — rendered with Angular Signals.

Built as a learning project focused on websocket fan-out, per-client subscription routing, RxJS/Signals interop, and resilient streaming — not as a trading tool.

## Architecture

```
Binance (public aggTrade stream)
        │  websocket, auto-reconnecting with backoff,
        │  supervised background task
        ▼
FastAPI backend
        │  ConnectionManager: tracks connected browsers AND
        │  each one's subscribed symbols; broadcasts every
        │  trade only to the browsers subscribed to that coin;
        │  isolates dead connections
        ▼
   /ws endpoint (one server, many browser clients)
     ▲     │
     │     ▼
  subscribe   trade
  messages    messages
     │     │
        ▼
Angular frontend
        │  checkboxes → send subscribe messages up the socket
        │  WebSocketSubject → map (parse numbers) → scan
        │  (track prev/current price per symbol) → auditTime
        │  (throttle renders to 2/sec) → toSignal → computed
        ▼
   Live PrimeNG table, one row per subscribed coin
```

**Why this shape:** a single persistent connection to Binance is fanned out to every connected browser from one backend process, rather than each browser polling independently. Each browser only receives the coins it subscribed to, so the backend filters per connection rather than blasting everything to everyone. The frontend keeps the underlying data fully accurate on every trade (via `scan`) while only *rendering* at a human-readable pace (via `auditTime`), so the table doesn't flicker faster than anyone can read it.

## Tech stack

**Backend:** Python, FastAPI, `websockets`, `certifi`, Pydantic, `pytest` + `pytest-asyncio`

**Frontend:** Angular 21 (standalone components), RxJS, Signals, TypeScript, PrimeNG, Vitest

## Features

- Tracks 10 symbols (BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, LINK) via Binance's combined `aggTrade` stream
- Automatic reconnection to Binance with exponential backoff on transient failures
- Supervised streaming task — if the background Binance stream dies, it's detected and restarted rather than silently stopping
- Per-client subscription routing — each browser subscribes to the symbols it wants via checkboxes, and the backend broadcasts each trade only to the connections subscribed to that coin
- Bidirectional websocket — the frontend sends subscribe messages up the same connection it reads trades from
- Pydantic validation of incoming subscribe messages — malformed messages are rejected without dropping the connection
- Fan-out to any number of connected browsers from a single upstream connection
- Per-connection failure isolation in broadcast — one dead browser tab doesn't affect others
- Live PrimeNG table with OnPush change detection: previous price, current price, delta (color-coded, directional arrow), quantity — throttled to two visual updates per second
- Test coverage on both sides — backend `ConnectionManager` (pytest, 5 scenarios) and frontend stream/table (Vitest, TestBed, fake timers, mocking)

## Running it locally

**Backend**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi-slim "uvicorn[standard]" websockets certifi pydantic pytest pytest-asyncio
uvicorn main:app --reload
```

Runs on `http://localhost:8000`. The Binance connection starts automatically on server startup.

**Frontend**

```bash
cd frontend
npm install
ng serve
```

Visit `http://localhost:4200`. Both servers need to be running for live data to appear.

**Tests**

```bash
# Backend
python -m pytest -v

# Frontend
cd frontend
npm run test
```

## Project structure

```
pulse/
├── main.py                      # FastAPI app, lifespan-managed background stream, /ws route
├── app/
│   ├── binance_client.py        # Binance connection: auto-reconnect, supervised task, broadcast
│   ├── connection_manager.py    # per-connection subscriptions (dict-based), filtered broadcast
│   ├── symbols.py               # tracked symbol list + validation
│   └── schemas.py               # Pydantic model(s) for incoming subscribe messages
├── tests/
│   └── test_connection_manager.py   # 5 scenarios
└── frontend/
    └── src/app/
        ├── trade-stream.ts      # WebSocketSubject → typed Trade stream; also sends subscribe messages
        ├── models/              # Trade, RawTrade, TradeRow interfaces
        └── trade-table/         # checkboxes + scan → auditTime → Signal → PrimeNG table (OnPush)
```

## Known limitations

This is a working project, not a finished product. Things that are explicitly *not* handled yet:

- Single backend instance only — no Redis pub/sub or multi-instance fan-out (
- No rate limiting on incoming subscribe messages
- Trades are not persisted — the dashboard is live-only, with no history or replay
