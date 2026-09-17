from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Mt5Config:
    enabled: bool = False
    terminal_path: Optional[str] = None
    login: Optional[int] = None
    password: Optional[str] = None
    server: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Mt5Config":
        return cls(
            enabled=os.getenv("MT5_ENABLED", "false").lower() in {"1", "true", "yes"},
            terminal_path=os.getenv("MT5_TERMINAL_PATH"),
            login=int(os.getenv("MT5_LOGIN", "0")) if os.getenv("MT5_LOGIN") else None,
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
        )


class MT5Connector:
    """MT5 adapter skeleton.

    This is intentionally disabled by default and does not perform live trading or
    order submission. It's a safe placeholder for future integration work.
    """

    def __init__(self, config: Optional[Mt5Config] = None):
        self.config = config or Mt5Config.from_env()

    @property
    def is_enabled(self) -> bool:
        return self.config.enabled

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.is_enabled,
            "mode": "disabled" if not self.is_enabled else "available",
            "terminal_path": self.config.terminal_path,
            "server": self.config.server,
            "message": "MT5 connector is disabled by default. Turn on only after safe validation and credentials handling.",
        }

    def connect(self) -> Dict[str, Any]:
        if not self.is_enabled:
            raise RuntimeError("MT5 connector is disabled. Set MT5_ENABLED=true only after validating a safe implementation.")
        return {"status": "connected"}

    def get_account_summary(self) -> Dict[str, Any]:
        if not self.is_enabled:
            raise RuntimeError("MT5 connector is disabled.")
        return {"balance": 0.0, "equity": 0.0, "currency": "USD"}

    def place_order(self, *args, **kwargs) -> Dict[str, Any]:
        if not self.is_enabled:
            raise RuntimeError("Live MT5 order placement is disabled in this build.")
        return {"status": "order_accepted"}
