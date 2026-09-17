# TradeForge

TradeForge is a local-first algorithmic trading platform scaffold designed to support:

- strategy definitions and parameter management
- market-data access through brokers or exchange adapters
- backtesting on historical price data
- paper trading with execution protections
- risk controls for max drawdown and position sizing

This repository is intentionally a working foundation for the first MVP. The app includes:

- a FastAPI backend
- a simple strategy model
- a risk engine
- a historical backtesting runner
- basic health and strategy endpoints
- a test suite covering the core logic

## Tech stack

- Python 3.11+
- FastAPI
- Pydantic
- NumPy / pandas
- pytest
- CCXT for exchange integrations

## Project layout

```text
app/
  api/
    routes/
  core/
  models/
  schemas/
  services/
  __init__.py
  main.py
tests/
requirements.txt
.env.example
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# or .venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Health check

```bash
curl http://localhost:8000/health
```

### Example strategy payload

```json
{
  "name": "MA Cross",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "capital": 10000,
  "buy_threshold": 0.6,
  "sell_threshold": 0.4,
  "fast_period": 5,
  "slow_period": 10,
  "enabled": true
}
```

## Current MVP scope

This initial release focuses on the operational foundation, not live exchange trading:

- create and view strategies
- run a simple SMA crossover backtest
- evaluate risk limits before trade execution
- simulate paper-trading decisions safely in code

## Next phases

- Binance execution adapter
- MetaTrader 5 bridge
- persistent database layer
- dashboard / UI
- AI-assisted strategy review
- real-time monitoring

