from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Strategy
from app.schemas.strategy_schema import StrategyCreate
from app.services.backtester import Backtester

router = APIRouter()


def serialize_strategy(row: Strategy) -> Dict[str, Any]:
    return {"id": row.id, "name": row.name, "symbol": row.symbol, "timeframe": row.timeframe, "capital": row.capital, "buy_threshold": row.buy_threshold, "sell_threshold": row.sell_threshold, "fast_period": row.fast_period, "slow_period": row.slow_period, "enabled": row.enabled}


@router.get("/strategies")
def list_strategies() -> List[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        return [serialize_strategy(row) for row in db.query(Strategy).all()]
    finally:
        db.close()


@router.post("/strategies")
def create_strategy(strategy: StrategyCreate) -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        row = Strategy(**strategy.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return serialize_strategy(row)
    finally:
        db.close()


@router.get("/strategies/{strategy_id}")
def get_strategy(strategy_id: int) -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        row = db.get(Strategy, strategy_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Strategy not found")
        return serialize_strategy(row)
    finally:
        db.close()


@router.post("/backtest")
def run_backtest(payload: Dict[str, Any]) -> Dict[str, Any]:
    candles = payload.get("candles", [])
    if not candles:
        raise HTTPException(status_code=400, detail="Candles are required for backtesting.")
    strategy = payload.get("strategy", {})
    result = Backtester(initial_capital=float(strategy.get("capital", 10000))).run(candles, fast_period=int(strategy.get("fast_period", 5)), slow_period=int(strategy.get("slow_period", 10)))
    return result.__dict__
