from fastapi import APIRouter, HTTPException

from app.models.strategy import StrategyConfig
from app.schemas.strategy_schema import StrategyCreate, StrategyResponse
from app.services.backtester import Backtester

router = APIRouter()

STORE: list[dict] = []


@router.get("/strategies", response_model=list[dict])
def list_strategies() -> list[dict]:
    return STORE


@router.post("/strategies", response_model=dict)
def create_strategy(strategy: StrategyCreate) -> dict:
    new_strategy = StrategyConfig(
        name=strategy.name,
        symbol=strategy.symbol,
        timeframe=strategy.timeframe,
        capital=strategy.capital,
        buy_threshold=strategy.buy_threshold,
        sell_threshold=strategy.sell_threshold,
        fast_period=strategy.fast_period,
        slow_period=strategy.slow_period,
        enabled=strategy.enabled,
        parameters=strategy.parameters,
    )
    item = {
        "id": len(STORE) + 1,
        "name": new_strategy.name,
        "symbol": new_strategy.symbol,
        "timeframe": new_strategy.timeframe,
        "capital": new_strategy.capital,
        "buy_threshold": new_strategy.buy_threshold,
        "sell_threshold": new_strategy.sell_threshold,
        "fast_period": new_strategy.fast_period,
        "slow_period": new_strategy.slow_period,
        "enabled": new_strategy.enabled,
        "parameters": new_strategy.parameters,
    }
    STORE.append(item)
    return item


@router.post("/backtest")
def run_backtest(payload: dict) -> dict:
    candles = payload.get("candles", [])
    if not candles:
        raise HTTPException(status_code=400, detail="Candles are required for backtesting.")

    strategy = payload.get("strategy", {})
    backtester = Backtester(initial_capital=float(strategy.get("capital", 10000)))
    result = backtester.run(candles, fast_period=int(strategy.get("fast_period", 5)), slow_period=int(strategy.get("slow_period", 10)))
    return {
        "total_return_pct": round(result.total_return_pct, 2),
        "win_rate": round(result.win_rate, 2),
        "profit_factor": round(result.profit_factor, 2),
        "max_drawdown_pct": round(result.max_drawdown_pct, 2),
        "trades": result.trades,
        "equity_curve": result.equity_curve,
    }
