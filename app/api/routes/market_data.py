from fastapi import APIRouter, HTTPException

from app.services.market_data import MarketDataService

router = APIRouter()


@router.get("/market-data/ohlcv")
def get_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100) -> dict:
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 1000")
    candles = MarketDataService().fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
    return {"symbol": symbol, "timeframe": timeframe, "count": len(candles), "candles": candles}
