from fastapi import APIRouter, HTTPException

from app.services.mt5_client import MT5Connector

router = APIRouter(prefix="/mt5", tags=["mt5"])


@router.get("/status")
def mt5_status() -> dict:
    connector = MT5Connector()
    return connector.status()


@router.post("/connect")
def mt5_connect() -> dict:
    connector = MT5Connector()
    try:
        return connector.connect()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/account")
def mt5_account() -> dict:
    connector = MT5Connector()
    try:
        return connector.get_account_summary()
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
