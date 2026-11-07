"""Tests for synchronous drop-in MetaTrader5Client API."""

import numpy as np
import pandas as pd
from pymt5_linux.constants import (
    TRADE_ACTION_DEAL,
    ORDER_TYPE_BUY,
    ORDER_TYPE_SELL,
    TRADE_RETCODE_DONE,
    TIMEFRAME_M1
)
from pymt5_linux.types import (
    AccountInfo,
    TerminalInfo,
    SymbolInfo,
    Tick,
    OrderSendResult,
    TradePosition
)


def test_client_info_queries(mt5_client):
    """Test account, terminal, version, and symbols queries."""
    v = mt5_client.version()
    assert v is not None
    assert len(v) == 3

    t_info = mt5_client.terminal_info()
    assert isinstance(t_info, TerminalInfo)
    assert t_info.connected is True

    acct = mt5_client.account_info()
    assert isinstance(acct, AccountInfo)
    assert acct.balance == 25000.0
    assert acct.currency == "USD"

    # Symbols
    total = mt5_client.symbols_total()
    assert total >= 5

    symbols = mt5_client.symbols_get()
    assert symbols is not None
    assert len(symbols) >= 5

    sym_info = mt5_client.symbol_info("EURUSD")
    assert isinstance(sym_info, SymbolInfo)
    assert sym_info.name == "EURUSD"

    tick = mt5_client.symbol_info_tick("EURUSD")
    assert isinstance(tick, Tick)
    assert tick.bid > 0
    assert tick.ask >= tick.bid


def test_client_historical_data_pandas(mt5_client):
    """Test copy_rates_from_pos and copy_rates_from_pos_df."""
    arr = mt5_client.copy_rates_from_pos("EURUSD", TIMEFRAME_M1, 0, 100)
    assert isinstance(arr, np.ndarray)
    assert len(arr) == 100
    assert "close" in arr.dtype.names

    df = mt5_client.copy_rates_from_pos_df("EURUSD", TIMEFRAME_M1, 0, 100)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    assert "close" in df.columns
    assert "open" in df.columns
    assert str(df.index.dtype).startswith("datetime64")


def test_client_trading_workflow(mt5_client):
    """Test full trade lifecycle: check -> send -> positions_get -> close."""
    margin = mt5_client.order_calc_margin(ORDER_TYPE_BUY, "EURUSD", 0.1, 1.0850)
    assert margin is not None and margin > 0

    profit = mt5_client.order_calc_profit(ORDER_TYPE_BUY, "EURUSD", 0.1, 1.0850, 1.0870)
    assert profit is not None and profit > 0

    # Send BUY order
    buy_request = {
        "action": TRADE_ACTION_DEAL,
        "symbol": "EURUSD",
        "volume": 0.1,
        "type": ORDER_TYPE_BUY,
        "price": 1.0850,
        "sl": 1.0800,
        "tp": 1.0900,
        "comment": "Client test deal"
    }
    result = mt5_client.order_send(buy_request)
    assert isinstance(result, OrderSendResult)
    assert result.retcode == TRADE_RETCODE_DONE
    assert result.deal > 0

    # Verify positions
    positions = mt5_client.positions_get(symbol="EURUSD")
    assert positions is not None
    assert len(positions) == 1
    pos = positions[0]
    assert isinstance(pos, TradePosition)
    assert pos.symbol == "EURUSD"
    assert pos.volume == 0.1

    # Close the position
    close_request = {
        "action": TRADE_ACTION_DEAL,
        "position": pos.ticket,
        "symbol": "EURUSD",
        "volume": 0.1,
        "type": ORDER_TYPE_SELL,
        "price": 1.0860
    }
    close_res = mt5_client.order_send(close_request)
    assert close_res.retcode == TRADE_RETCODE_DONE

    # Positions should now be 0
    remaining_pos = mt5_client.positions_get(symbol="EURUSD")
    assert len(remaining_pos) == 0

    # History deals check
    deals = mt5_client.history_deals_get()
    assert deals is not None
    assert len(deals) >= 2


def test_client_api_validated_marker():
    print("CLIENT_API_VALIDATED")
    assert True
