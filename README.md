# TradeForge

This repo is a local-first trading platform foundation with safe paper-trading and market-data support.

## Features in this branch

- Strategy definition and persistence in SQLite
- SMA crossover backtesting
- Binance public OHLCV market-data access via CCXT
- Paper-trading simulation layer
- MT5 adapter skeleton kept disabled by default
- FastAPI API for local testing

## MT5 status

MetaTrader 5 integration is intentionally included as a skeleton only.

- `MT5_ENABLED` defaults to `false`
- no live order submission is active
- no real credentials are required for the default setup
- live MT5 integrations must be guarded by explicit configuration, secure secrets, and strict validation before enabling

## Local quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000/docs

### MT5-related endpoints

- `GET /mt5/status`
- `POST /mt5/connect`
- `GET /mt5/account`

These endpoints return a disabled state until MT5 is explicitly enabled and configured.

## Safety rules

- never enable live trading without secure secret management
- never execute real trades in development without risk limits and validation
- keep the MT5 adapter behind a disabled default
