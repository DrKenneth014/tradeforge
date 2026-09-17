from __future__ import annotations

from typing import Any, Dict, List


class PaperTradingEngine:
    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def simulate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        entry = float(payload.get("entry_price", 0))
        exit_price = float(payload.get("exit_price", 0))
        if entry <= 0 or exit_price <= 0:
            raise ValueError("entry_price and exit_price must be positive")
        side = payload.get("side", "long").lower()
        if side not in {"long", "short"}:
            raise ValueError("side must be long or short")
        pnl_pct = ((exit_price - entry) / entry if side == "long" else (entry - exit_price) / entry) * 100
        trade = {"strategy_name": payload.get("strategy_name", "manual"), "symbol": payload.get("symbol", "BTC/USDT"), "side": side, "entry_price": entry, "exit_price": exit_price, "pnl_pct": round(pnl_pct, 4), "status": "closed"}
        self.history.append(trade)
        return trade
