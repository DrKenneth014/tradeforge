from app.services.paper_trading import PaperTradingEngine


def test_paper_trading_engine_simulates_trade():
    engine = PaperTradingEngine()
    result = engine.simulate({
        "strategy_name": "MA Cross",
        "symbol": "BTC/USDT",
        "entry_price": 100.0,
        "exit_price": 110.0,
    })

    assert result["symbol"] == "BTC/USDT"
    assert result["status"] == "closed"
    assert result["pnl_pct"] > 0
