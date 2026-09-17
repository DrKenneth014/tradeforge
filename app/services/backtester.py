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
        return [float("nan") if len(values[max(0, i - period + 1):i + 1]) < period else sum(values[max(0, i - period + 1):i + 1]) / period for i in range(len(values))]

    def run(self, candles: List[Dict[str, Any]], *, fast_period: int = 5, slow_period: int = 10) -> BacktestResult:
        if fast_period < 2 or slow_period < 2:
            raise ValueError("Moving-average periods must be at least 2")
        closes = [float(candle["close"]) for candle in candles]
        if not closes:
            return BacktestResult(0.0, 0.0, 0.0, 0.0, 0, [self.initial_capital])
        fast, slow = self._sma(closes, fast_period), self._sma(closes, slow_period)
        position, entry, pnls = 0, 0.0, []
        for i in range(1, len(closes)):
            vals = [fast[i - 1], slow[i - 1], fast[i], slow[i]]
            if any(math.isnan(v) for v in vals):
                continue
            if position == 0:
                if fast[i] > slow[i] and fast[i - 1] <= slow[i - 1]: position, entry = 1, closes[i]
                elif fast[i] < slow[i] and fast[i - 1] >= slow[i - 1]: position, entry = -1, closes[i]
            elif (position == 1 and fast[i] < slow[i] and fast[i - 1] >= slow[i - 1]) or (position == -1 and fast[i] > slow[i] and fast[i - 1] <= slow[i - 1]):
                pnls.append((closes[i] - entry) / entry if position == 1 else (entry - closes[i]) / entry)
                position = 0
        if position:
            pnls.append((closes[-1] - entry) / entry if position == 1 else (entry - closes[-1]) / entry)
        wins = sum(p > 0 for p in pnls)
        gross_profit, gross_loss = sum(p for p in pnls if p > 0), abs(sum(p for p in pnls if p < 0))
        equity = [self.initial_capital]
        cumulative = 0.0
        for pnl in pnls:
            cumulative += pnl
            equity.append(self.initial_capital * (1 + cumulative))
        peak = equity[0]
        drawdown = 0.0
        for value in equity:
            peak = max(peak, value)
            drawdown = max(drawdown, (peak - value) / peak if peak else 0.0)
        return BacktestResult(sum(pnls) * 100, wins / len(pnls) * 100 if pnls else 0.0, gross_profit / gross_loss if gross_loss else 0.0, drawdown * 100, len(pnls), equity)
