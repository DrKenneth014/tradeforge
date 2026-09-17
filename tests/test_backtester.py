from app.services.backtester import Backtester


def test_backtester_produces_metrics_for_sample_candles():
    candles = [
        {"close": 100.0},
        {"close": 101.0},
        {"close": 102.0},
        {"close": 101.0},
        {"close": 103.0},
        {"close": 104.0},
        {"close": 103.0},
        {"close": 105.0},
        {"close": 106.0},
        {"close": 107.0},
        {"close": 108.0},
        {"close": 110.0},
    ]

    backtester = Backtester(initial_capital=10000)
    result = backtester.run(candles, fast_period=2, slow_period=3)

    assert result.trades >= 0
    assert isinstance(result.total_return_pct, float)
    assert isinstance(result.max_drawdown_pct, float)
    assert result.equity_curve
