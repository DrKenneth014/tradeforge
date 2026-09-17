from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StrategyConfig:
    name: str
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    capital: float = 10000.0
    buy_threshold: float = 0.6
    sell_threshold: float = 0.4
    fast_period: int = 5
    slow_period: int = 10
    enabled: bool = True
    parameters: dict = field(default_factory=dict)

    @property
    def risk_per_trade(self) -> float:
        return self.capital * 0.01


@dataclass
class TradeSignal:
    signal: int
    price: float
    timestamp: Optional[str] = None
