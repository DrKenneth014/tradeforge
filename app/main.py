from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.strategies import router as strategy_router
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(health_router)
app.include_router(strategy_router)


@app.get("/")
def root() -> dict:
    return {"message": f"Welcome to {settings.app_name}", "environment": settings.environment}
