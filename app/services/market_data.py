from __future__ import annotations

from typing import Any, Dict, List

import ccxt


class MarketDataService:
    def __init__(self, exchange_name: str = "binance") -> None:
        if not hasattr(ccxt, exchange_name):
            raise ValueError(f"Unsupported exchange: {exchange_name}")
        self.exchange = getattr(ccxt, exchange_name)({"enableRateLimit": True})

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[Dict[str, Any]]:
        candles = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return [{"timestamp": c[0], "open": float(c[1]), "high": float(c[2]), "low": float(c[3]), "close": float(c[4]), "volume": float(c[5])} for c in candles]
