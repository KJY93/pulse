# Pulse

A real-time cryptocurrency trade dashboard. Live trades from Binance flow through a Python backend and out to any number of connected browsers over a websocket, rendered with Angular Signals.

Built as a learning project focused on websocket fan-out, RxJS/Signals interop, and resilient streaming — not as a trading tool.

## Architecture

```
Binance (public aggTrade stream)
        │  websocket, auto-reconnecting with backoff
        ▼
FastAPI backend
        │  ConnectionManager: tracks connected browsers,
        │  broadcasts to all of them, isolates dead connections
        ▼
   /ws endpoint (one server, many browser clients)
        │
        ▼
Angular frontend
        │  WebSocketSubject → map (parse numbers) → scan
        │  (track prev/current price per symbol) → auditTime
        │  (throttle renders to 2/sec) → toSignal → computed
        ▼
   Live table, one row per tracked coin
```

**Why this shape:** a single persistent connection to Binance is fanned out to every connected browser from one backend process, rather than each browser polling independently. The frontend keeps the underlying data fully accurate on every trade (via `scan`) while only *rendering* at a human-readable pace (via `auditTime`), so the table doesn't flicker faster than anyone can read it.

## Tech stack

**Backend:** Python, FastAPI, `websockets`, `certifi`, `pytest` + `pytest-asyncio`

**Frontend:** Angular 21 (standalone components), RxJS, Signals, TypeScript

## Features

- Tracks 10 symbols (BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, LINK) via Binance's combined `aggTrade` stream
- Automatic reconnection to Binance with exponential backoff on transient failures
- Fan-out to any number of connected browsers from a single upstream connection
- Per-connection failure isolation in broadcast — one dead browser tab doesn't affect others
- Live table: previous price, current price, delta (color-coded, directional arrow), quantity — throttled to one visual update per second
- Full test coverage on `ConnectionManager` (connect, disconnect, broadcast, and broadcast-with-partial-failure)

## Running it locally

**Backend**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi-slim "uvicorn[standard]" websockets certifi pytest pytest-asyncio
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
python -m pytest -v
```

## Project structure

```
pulse/
├── main.py                  # FastAPI app, lifespan-managed background stream
├── app/
│   ├── binance_client.py    # Connects to Binance, auto-reconnects, broadcasts
│   └── connection_manager.py
├── tests/
│   └── test_connection_manager.py
└── frontend/
    └── src/app/
        ├── trade-stream.ts       # WebSocketSubject → typed Trade stream
        ├── models/               # Trade, RawTrade, TradeRow interfaces
        └── trade-table/          # scan → auditTime → Signal → table
```

## Known limitations

This is a working v1, not a finished product. Things that are explicitly *not* handled yet:

- If the background Binance-streaming task dies from a non-retryable error, nothing currently detects or restarts it — the server keeps running, but trade data silently stops
- All browsers receive all 10 symbols; there's no per-client subscription/filtering
- Single-instance only — scaling to multiple backend processes at once isn't implemented
- No frontend test suite yet (backend is fully tested; frontend isn't)
- Table styling is hand-rolled HTML/CSS rather than a component library
