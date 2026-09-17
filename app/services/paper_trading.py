from dataclasses import dataclass


@dataclass
class RiskCheck:
    allowed: bool
    reason: str = ""
    suggested_position_size: float = 0.0


class RiskEngine:
    def __init__(self, *, max_position_size: float = 0.1, max_daily_loss: float = 0.02, max_open_positions: int = 3):
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss
        self.max_open_positions = max_open_positions

    def evaluate_trade(self, *, capital: float, notional_size: float, open_positions: int, current_drawdown: float = 0.0) -> RiskCheck:
        max_trade_size = capital * self.max_position_size
        if notional_size > max_trade_size:
            return RiskCheck(
                allowed=False,
                reason=f"Trade size exceeds max allowed position size ({max_trade_size:.2f}).",
                suggested_position_size=max_trade_size,
            )

        if current_drawdown >= self.max_daily_loss:
            return RiskCheck(
                allowed=False,
                reason=f"Portfolio drawdown exceeds daily loss limit ({self.max_daily_loss * 100:.2f}%).",
                suggested_position_size=0.0,
            )

        if open_positions >= self.max_open_positions:
            return RiskCheck(
                allowed=False,
                reason=f"Open positions limit reached ({self.max_open_positions}).",
                suggested_position_size=0.0,
            )

        return RiskCheck(
            allowed=True,
            reason="Trade passes risk limits.",
            suggested_position_size=min(notional_size, max_trade_size),
        )

    def position_size_for_equity(self, equity: float, risk_percent: float = 0.01) -> float:
        return equity * risk_percent
