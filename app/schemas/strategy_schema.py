from typing import Optional
from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    capital: float = Field(10000.0, gt=0)
    buy_threshold: float = Field(0.6, ge=0, le=1)
    sell_threshold: float = Field(0.4, ge=0, le=1)
    fast_period: int = Field(5, ge=2)
    slow_period: int = Field(10, ge=2)
    enabled: bool = True


class StrategyResponse(StrategyCreate):
    id: int
    created_at: Optional[str] = None
