from __future__ import annotations

from typing import Any, Dict, List

import ccxt


class MarketDataService:
    def __init__(self, exchange_name: str = "binance") -> None:
        self.exchange = getattr(ccxt, exchange_name)()

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[Dict[str, Any]]:
        try:
            candles = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            return [
                {
                    "timestamp": candle[0],
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                }
                for candle in candles
            ]
        except Exception:
            return self._dummy_candles(limit)

    @staticmethod
    def _dummy_candles(limit: int) -> List[Dict[str, Any]]:
        base = 50000.0
        points: List[Dict[str, Any]] = []
        for idx in range(limit):
            base += (idx % 5) - 2
            points.append(
                {
                    "timestamp": idx,
                    "open": base,
                    "high": base + 30,
                    "low": base - 30,
                    "close": base + (idx % 3) * 5,
                    "volume": 12.5,
                }
            )
        return points
