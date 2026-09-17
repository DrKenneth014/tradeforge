from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class BacktestResult:
    total_return_pct: float
    win_rate: float
    profit_factor: float
    max_drawdown_pct: float
    trades: int
    equity_curve: List[float]


class Backtester:
    def __init__(self, *, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital

    def _sma(self, values: List[float], period: int) -> List[float]:
        result: List[float] = []
        for index in range(len(values)):
            window = values[max(0, index - period + 1):index + 1]
            if len(window) < period:
                result.append(float("nan"))
            else:
                result.append(sum(window) / len(window))
        return result

    def run(self, candles: List[Dict[str, Any]], *, fast_period: int = 5, slow_period: int = 10) -> BacktestResult:
        closes = [float(candle["close"]) for candle in candles]
        fast = self._sma(closes, fast_period)
        slow = self._sma(closes, slow_period)

        equity = self.initial_capital
        position = 0
        entry_price = 0.0
        trades = 0
        pnl_values: List[float] = []
        wins = 0
        gross_profit = 0.0
        gross_loss = 0.0

        for index in range(1, len(closes)):
            prev_fast = fast[index - 1]
            prev_slow = slow[index - 1]
            current_fast = fast[index]
            current_slow = slow[index]

            if position == 0 and not (float("nan") in [prev_fast, prev_slow, current_fast, current_slow]):
                if current_fast > current_slow and prev_fast <= prev_slow:
                    position = 1
                    entry_price = closes[index]
                elif current_fast < current_slow and prev_fast >= prev_slow:
                    position = -1
                    entry_price = closes[index]

            elif position != 0 and not (float("nan") in [prev_fast, prev_slow, current_fast, current_slow]):
                if position == 1 and current_fast < current_slow and prev_fast >= prev_slow:
                    exit_price = closes[index]
                    trade_pnl = (exit_price - entry_price) / entry_price
                    pnl_values.append(trade_pnl)
                    trades += 1
                    if trade_pnl > 0:
                        wins += 1
                        gross_profit += trade_pnl
                    else:
                        gross_loss += abs(trade_pnl)
                    position = 0
                elif position == -1 and current_fast > current_slow and prev_fast <= prev_slow:
                    exit_price = closes[index]
                    trade_pnl = (entry_price - exit_price) / entry_price
                    pnl_values.append(trade_pnl)
                    trades += 1
                    if trade_pnl > 0:
                        wins += 1
                        gross_profit += trade_pnl
                    else:
                        gross_loss += abs(trade_pnl)
                    position = 0

        if position != 0 and closes:
            exit_price = closes[-1]
            trade_pnl = (exit_price - entry_price) / entry_price if position == 1 else (entry_price - exit_price) / entry_price
            pnl_values.append(trade_pnl)
            trades += 1
            if trade_pnl > 0:
                wins += 1
                gross_profit += trade_pnl
            else:
                gross_loss += abs(trade_pnl)

        total_return = sum(pnl_values)
        total_return_pct = total_return * 100
        win_rate = (wins / trades) * 100 if trades else 0.0
        profit_factor = gross_profit / gross_loss if gross_loss else float("inf")

        equity_curve = [self.initial_capital * (1 + cumulative) for cumulative in self._cumulative_returns(pnl_values)]
        max_drawdown_pct = self._max_drawdown(equity_curve)

        return BacktestResult(
            total_return_pct=total_return_pct,
            win_rate=win_rate,
            profit_factor=profit_factor,
            max_drawdown_pct=max_drawdown_pct,
            trades=trades,
            equity_curve=equity_curve,
        )

    def _cumulative_returns(self, pnl_values: List[float]) -> List[float]:
        cumulative = 0.0
        values: List[float] = []
        for pnl in pnl_values:
            cumulative += pnl
            values.append(cumulative)
        return values

    def _max_drawdown(self, equity_curve: List[float]) -> float:
        if not equity_curve:
            return 0.0
        peak = equity_curve[0]
        max_drawdown = 0.0
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak if peak else 0.0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown * 100
