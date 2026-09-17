from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.market_data import router as market_data_router
from app.api.routes.mt5 import router as mt5_router
from app.api.routes.paper_trading import router as paper_trading_router
from app.api.routes.strategies import router as strategy_router
from app.core.config import settings
from app.db.database import Base, engine
from app.db import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="0.3.0")
app.include_router(health_router)
app.include_router(strategy_router)
app.include_router(market_data_router)
app.include_router(paper_trading_router)
app.include_router(mt5_router)


@app.get("/")
def root() -> dict:
    return {"message": f"Welcome to {settings.app_name}", "environment": settings.environment}
