from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from app.services.paper_trading import PaperTradingEngine

router = APIRouter()
_engine = PaperTradingEngine()


@router.get("/paper-trades")
def list_paper_trades() -> List[Dict[str, Any]]:
    return _engine.history


@router.post("/paper-trades/simulate")
def simulate_paper_trade(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _engine.simulate(payload)
