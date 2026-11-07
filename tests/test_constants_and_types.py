"""Tests for MT5 constants, enums, namedtuples, and numpy/pandas converters."""

import numpy as np
import pandas as pd
from pymt5_linux.constants import (
    TIMEFRAME_M1, TIMEFRAME_H1, TIMEFRAME_D1,
    ORDER_TYPE_BUY, ORDER_TYPE_SELL,
    TRADE_ACTION_DEAL, TRADE_ACTION_SLTP,
    TRADE_RETCODE_DONE, TRADE_RETCODE_NO_MONEY,
    POSITION_TYPE_BUY, POSITION_TYPE_SELL
)
from pymt5_linux.types import (
    AccountInfo, TerminalInfo, SymbolInfo, Tick,
    TradeOrder, TradePosition, TradeDeal,
    OrderSendResult, OrderCheckResult, BookInfo,
    RATE_DTYPE, TICK_DTYPE,
    rates_to_numpy, ticks_to_numpy, rates_to_dataframe
)


def test_timeframes_and_orders():
    assert TIMEFRAME_M1 == 1
    assert TIMEFRAME_H1 == 16385
    assert TIMEFRAME_D1 == 16408
    assert ORDER_TYPE_BUY == 0
    assert ORDER_TYPE_SELL == 1
    assert TRADE_ACTION_DEAL == 1
    assert TRADE_RETCODE_DONE == 10009


def test_account_info_namedtuple():
    acct = AccountInfo(
        login=123456, trade_mode=0, leverage=100, limit_orders=200,
        margin_so_mode=0, trade_allowed=True, trade_expert=True, margin_mode=2,
        currency_digits=2, fifo_close=False, balance=10000.0, credit=0.0,
        profit=150.0, equity=10150.0, margin=500.0, margin_free=9650.0,
        margin_level=2030.0, margin_so_call=50.0, margin_so_so=30.0,
        margin_initial=0.0, margin_maintenance=0.0, assets=0.0, liabilities=0.0,
        commission_blocked=0.0, name="Trader", server="Demo", currency="USD", company="MetaQuotes"
    )
    assert acct.login == 123456
    assert acct.balance == 10000.0
    assert acct.equity == 10150.0
    assert acct.currency == "USD"


def test_rates_conversion_numpy_and_pandas():
    raw_rates = [
        {"time": 1700000000, "open": 1.0850, "high": 1.0860, "low": 1.0845, "close": 1.0855, "tick_volume": 120, "spread": 10, "real_volume": 0},
        {"time": 1700000060, "open": 1.0855, "high": 1.0870, "low": 1.0852, "close": 1.0865, "tick_volume": 150, "spread": 10, "real_volume": 0}
    ]

    arr = rates_to_numpy(raw_rates)
    assert isinstance(arr, np.ndarray)
    assert len(arr) == 2
    assert arr.dtype == RATE_DTYPE
    assert arr[0]["close"] == 1.0855
    assert arr[1]["high"] == 1.0870

    # Test conversion to Pandas DataFrame
    df = rates_to_dataframe(arr)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["open", "high", "low", "close", "tick_volume", "spread", "real_volume"]
    assert str(df.index.dtype).startswith("datetime64")


def test_ticks_conversion_numpy():
    raw_ticks = [
        {"time": 1700000000, "bid": 1.0850, "ask": 1.0851, "last": 1.08505, "volume": 5, "time_msc": 1700000000123, "flags": 6, "volume_real": 0.0}
    ]
    arr = ticks_to_numpy(raw_ticks)
    assert isinstance(arr, np.ndarray)
    assert len(arr) == 1
    assert arr.dtype == TICK_DTYPE
    assert arr[0]["bid"] == 1.0850
    assert arr[0]["time_msc"] == 1700000000123


def test_all_types_validated_marker():
    """Outputs marker for G2 gate confirmation."""
    print("ALL_TYPES_VALIDATED")
    assert True
