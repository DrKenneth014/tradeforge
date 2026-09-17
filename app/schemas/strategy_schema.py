from typing import Optional

from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    symbol: str = Field(default="BTC/USDT")
    timeframe: str = Field(default="1h")
    capital: float = Field(default=10000.0, gt=0)
    buy_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
    sell_threshold: float = Field(default=0.4, ge=0.0, le=1.0)
    fast_period: int = Field(default=5, ge=2)
    slow_period: int = Field(default=10, ge=2)
    enabled: bool = True


class StrategyResponse(StrategyCreate):
    id: int
    created_at: Optional[str] = None
