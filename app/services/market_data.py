from __future__ import annotations

from typing import Any, Dict, List


class PaperTradingEngine:
    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def simulate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        strategy_name = payload.get("strategy_name", "MA Cross")
        symbol = payload.get("symbol", "BTC/USDT")
        entry_price = float(payload.get("entry_price", 100.0))
        exit_price = float(payload.get("exit_price", 105.0))
        pnl = (exit_price - entry_price) / entry_price * 100

        trade = {
            "strategy_name": strategy_name,
            "symbol": symbol,
            "side": "long",
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl_pct": round(pnl, 2),
            "status": "closed",
        }
        self.history.append(trade)
        return trade
