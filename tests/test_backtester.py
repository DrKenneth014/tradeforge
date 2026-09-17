from app.services.risk_engine import RiskEngine


def test_risk_engine_allows_standard_trade():
    engine = RiskEngine(max_position_size=0.10, max_daily_loss=0.05, max_open_positions=3)
    result = engine.evaluate_trade(capital=10000, notional_size=500, open_positions=1)
    assert result.allowed is True
    assert result.suggested_position_size == 500


def test_risk_engine_blocks_large_trade():
    engine = RiskEngine(max_position_size=0.10, max_daily_loss=0.05, max_open_positions=3)
    result = engine.evaluate_trade(capital=10000, notional_size=1500, open_positions=1)
    assert result.allowed is False
    assert result.suggested_position_size == 1000


def test_risk_engine_blocks_max_open_positions():
    engine = RiskEngine(max_position_size=0.10, max_daily_loss=0.05, max_open_positions=2)
    result = engine.evaluate_trade(capital=10000, notional_size=500, open_positions=2)
    assert result.allowed is False
