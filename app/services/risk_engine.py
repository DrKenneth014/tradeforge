from __future__ import annotations

import math
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

    @staticmethod
    def _sma(values: List[float], period: int) -> List[float]:
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
        if not closes:
            return BacktestResult(
                total_return_pct=0.0,
                win_rate=0.0,
                profit_factor=0.0,
                max_drawdown_pct=0.0,
                trades=0,
                equity_curve=[self.initial_capital],
            )

        fast = self._sma(closes, fast_period)
        slow = self._sma(closes, slow_period)

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

            signal_values = [prev_fast, prev_slow, current_fast, current_slow]
            if position == 0 and all(not math.isnan(v) for v in signal_values):
                if current_fast > current_slow and prev_fast <= prev_slow:
                    position = 1
                    entry_price = closes[index]
                elif current_fast < current_slow and prev_fast >= prev_slow:
                    position = -1
                    entry_price = closes[index]
            elif position != 0 and all(not math.isnan(v) for v in signal_values):
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

        cumulative = 0.0
        equity_curve = [self.initial_capital]
        for pnl in pnl_values:
            cumulative += pnl
            equity_curve.append(self.initial_capital * (1 + cumulative))

        return BacktestResult(
            total_return_pct=total_return_pct,
            win_rate=win_rate,
            profit_factor=profit_factor,
            max_drawdown_pct=self._max_drawdown(equity_curve),
            trades=trades,
            equity_curve=equity_curve,
        )

    @staticmethod
    def _max_drawdown(equity_curve: List[float]) -> float:
        if len(equity_curve) < 2:
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
