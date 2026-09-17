# TradeForge

The current branch provides a local-first, **paper-trading-only** MVP foundation.

## Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API.

## Available operations

- `GET /health` — service status; live trading is deliberately disabled.
- `POST /strategies`, `GET /strategies`, `GET /strategies/{id}` — persist strategies in SQLite.
- `POST /backtest` — run a simple SMA crossover backtest over supplied candles.
- `GET /market-data/ohlcv` — fetch public Binance OHLCV data through CCXT. This does not need API keys.
- `POST /paper-trades/simulate` — simulate long or short trades without sending orders.
- `GET /paper-trades` — view paper trades from the current process.

## Safety boundary

No live order submission is implemented. Do not add exchange secrets or real-money execution until authentication, encrypted secret storage, order validation, kill switches, reconciliation, monitoring, and extensive paper-trading tests are in place.
