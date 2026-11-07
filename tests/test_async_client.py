"""Tests for AsyncMetaTrader5 and MT5Streamer."""

import pytest
import asyncio
import time
from pymt5_linux.async_client import AsyncMetaTrader5
from pymt5_linux.streaming import MT5Streamer
from pymt5_linux.constants import TIMEFRAME_M1, TRADE_ACTION_DEAL, ORDER_TYPE_BUY, TRADE_RETCODE_DONE
from pymt5_linux.types import AccountInfo, SymbolInfo, Tick


@pytest.mark.asyncio
async def test_async_client_lifecycle(running_mock_gateway):
    host, port = running_mock_gateway
    client = AsyncMetaTrader5(host=host, port=port)
    connected = await client.initialize()
    assert connected is True

    try:
        acct = await client.account_info()
        assert isinstance(acct, AccountInfo)
        assert acct.balance > 0

        sym = await client.symbol_info("EURUSD")
        assert isinstance(sym, SymbolInfo)

        tick = await client.symbol_info_tick("EURUSD")
        assert isinstance(tick, Tick)

        df = await client.copy_rates_from_pos_df("EURUSD", TIMEFRAME_M1, 0, 50)
        assert len(df) == 50

        # Send test order
        res = await client.order_send({
            "action": TRADE_ACTION_DEAL,
            "symbol": "EURUSD",
            "volume": 0.05,
            "type": ORDER_TYPE_BUY,
            "price": 1.0850
        })
        assert res.retcode == TRADE_RETCODE_DONE
    finally:
        await client.shutdown()


def test_streaming_ticks(mt5_client):
    streamer = MT5Streamer(mt5_client, poll_interval=0.05)
    received_ticks = []

    @streamer.on_tick("EURUSD")
    def on_tick(tick):
        received_ticks.append(tick)

    streamer.start()
    time.sleep(0.3)
    streamer.stop()

    assert len(received_ticks) >= 1
    assert received_ticks[0].bid > 0
