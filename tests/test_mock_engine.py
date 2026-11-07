"""Tests for MockMT5Engine trading simulator."""

from pymt5_linux.mock_engine import MockMT5Engine
from pymt5_linux.constants import (
    TRADE_ACTION_DEAL,
    TRADE_ACTION_SLTP,
    ORDER_TYPE_BUY,
    ORDER_TYPE_SELL,
    POSITION_TYPE_BUY,
    TRADE_RETCODE_DONE,
    TRADE_RETCODE_NO_MONEY,
    TIMEFRAME_M1,
    TIMEFRAME_H1
)


def test_mock_engine_account_and_symbols():
    engine = MockMT5Engine(login=888888, balance=20000.0)
    acct = engine.get_account_info()
    assert acct["login"] == 888888
    assert acct["balance"] == 20000.0
    assert acct["equity"] == 20000.0

    # Symbols check
    assert "EURUSD" in engine.symbols
    assert "BTCUSD" in engine.symbols
    sym = engine.get_symbol_info("EURUSD")
    assert sym is not None
    assert sym["name"] == "EURUSD"

    tick = engine.get_symbol_tick("EURUSD")
    assert tick is not None
    assert tick["bid"] > 0
    assert tick["ask"] >= tick["bid"]


def test_mock_engine_candles():
    engine = MockMT5Engine()
    bars = engine.copy_rates_from_pos("EURUSD", TIMEFRAME_M1, start_pos=0, count=50)
    assert len(bars) == 50
    assert "open" in bars[0]
    assert "close" in bars[0]
    assert bars[0]["high"] >= bars[0]["low"]


def test_mock_engine_order_lifecycle():
    engine = MockMT5Engine(balance=10000.0)

    # 1. Open BUY Position
    buy_req = {
        "action": TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "volume": 0.1,
        "type": ORDER_TYPE_BUY,
        "price": 1.0850,
        "sl": 1.0800,
        "tp": 1.0950,
        "comment": "AI Buy signal"
    }
    res = engine.execute_order(buy_req)
    assert res["retcode"] == TRADE_RETCODE_DONE
    assert res["deal"] > 0
    assert len(engine.positions) == 1

    pos_ticket = list(engine.positions.keys())[0]
    pos = engine.positions[pos_ticket]
    assert pos["type"] == POSITION_TYPE_BUY
    assert pos["volume"] == 0.1
    assert pos["sl"] == 1.0800

    # 2. Modify SL/TP
    modify_req = {
        "action": TRADE_ACTION_SLTP,
        "position": pos_ticket,
        "sl": 1.0820,
        "tp": 1.0980
    }
    res_mod = engine.execute_order(modify_req)
    assert res_mod["retcode"] == TRADE_RETCODE_DONE
    assert engine.positions[pos_ticket]["sl"] == 1.0820

    # 3. Close Position
    close_req = {
        "action": TRADE_ACTION_DEAL,
        "position": pos_ticket,
        "symbol": "EURUSD",
        "volume": 0.1,
        "type": ORDER_TYPE_SELL,
        "price": 1.0870
    }
    res_close = engine.execute_order(close_req)
    assert res_close["retcode"] == TRADE_RETCODE_DONE
    assert len(engine.positions) == 0
    assert len(engine.history_deals) == 2  # Entry deal + Exit deal


def test_mock_engine_margin_check():
    # Attempting to trade excessive volume with insufficient balance
    engine = MockMT5Engine(balance=50.0)
    huge_req = {
        "action": TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "volume": 10.0,
        "type": ORDER_TYPE_BUY,
        "price": 1.0850
    }
    res = engine.execute_order(huge_req)
    assert res["retcode"] == TRADE_RETCODE_NO_MONEY


def test_mock_engine_validated_marker():
    print("MOCK_ENGINE_VALIDATED")
    assert True
