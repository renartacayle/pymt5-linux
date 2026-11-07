"""Asynchronous MetaTrader 5 client for modern asyncio and concurrent trading bots."""

import asyncio
import uuid
import datetime
import logging
from typing import Optional, Tuple, Union, List, Dict, Any
import numpy as np
import pandas as pd

from .protocol import async_send_packet, async_receive_packet
from .constants import TIMEFRAME_M1, COPY_TICKS_ALL
from .errors import RES_S_OK, RES_E_FAIL, RES_E_INTERNAL_FAIL_CONNECT, format_error
from .types import (
    AccountInfo,
    TerminalInfo,
    SymbolInfo,
    Tick,
    TradeOrder,
    TradePosition,
    TradeDeal,
    OrderSendResult,
    OrderCheckResult,
    rates_to_numpy,
    ticks_to_numpy,
    rates_to_dataframe
)

logger = logging.getLogger("pymt5_linux.async_client")


class AsyncMetaTrader5:
    """Asynchronous client for MetaTrader 5 with non-blocking I/O."""

    def __init__(self, host: str = "127.0.0.1", port: int = 18812) -> None:
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self._connected = False
        self._last_err = (RES_S_OK, "Success")
        self._lock = asyncio.Lock()

    def last_error(self) -> Tuple[int, str]:
        return self._last_err

    def _set_error(self, code: int, msg: str = "") -> None:
        self._last_err = format_error(code, msg)

    async def initialize(self, host: Optional[str] = None, port: Optional[int] = None) -> bool:
        """Connect asynchronously to MT5 Gateway."""
        if host:
            self.host = host
        if port:
            self.port = port

        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self._connected = True
            res = await self._rpc_call("initialize", {})
            return bool(res)
        except Exception as e:
            self._set_error(RES_E_INTERNAL_FAIL_CONNECT, f"Async connect failed: {e}")
            self._connected = False
            return False

    async def shutdown(self) -> None:
        """Close connection asynchronously."""
        if self._connected and self.writer:
            try:
                await self._rpc_call("shutdown", {})
            except Exception:
                pass
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass
            self._connected = False
            self.reader = None
            self.writer = None

    async def _rpc_call(self, method: str, params: Any = None) -> Any:
        if not self._connected or not self.writer or not self.reader:
            self._set_error(RES_E_INTERNAL_FAIL_CONNECT, "Client is not connected")
            return None

        req_id = str(uuid.uuid4())
        packet = {"id": req_id, "method": method, "params": params or {}}

        async with self._lock:
            try:
                await async_send_packet(self.writer, packet)
                resp = await async_receive_packet(self.reader)
                if resp.get("error"):
                    err = resp["error"]
                    self._set_error(err.get("code", RES_E_FAIL), err.get("message", ""))
                    return None
                self._set_error(RES_S_OK, "Success")
                return resp.get("result")
            except Exception as e:
                self._set_error(RES_E_INTERNAL_FAIL_CONNECT, f"Async RPC communication error: {e}")
                self._connected = False
                return None

    async def account_info(self) -> Optional[AccountInfo]:
        res = await self._rpc_call("account_info")
        return AccountInfo(**res) if res and isinstance(res, dict) else None

    async def terminal_info(self) -> Optional[TerminalInfo]:
        res = await self._rpc_call("terminal_info")
        return TerminalInfo(**res) if res and isinstance(res, dict) else None

    async def symbol_info(self, symbol: str) -> Optional[SymbolInfo]:
        res = await self._rpc_call("symbol_info", {"symbol": symbol})
        return SymbolInfo(**res) if res and isinstance(res, dict) else None

    async def symbol_info_tick(self, symbol: str) -> Optional[Tick]:
        res = await self._rpc_call("symbol_info_tick", {"symbol": symbol})
        return Tick(**res) if res and isinstance(res, dict) else None

    async def copy_rates_from_pos(self, symbol: str, timeframe: int, start_pos: int, count: int) -> Optional[np.ndarray]:
        res = await self._rpc_call("copy_rates_from_pos", {
            "symbol": symbol, "timeframe": timeframe, "start_pos": start_pos, "count": count
        })
        return rates_to_numpy(res) if res is not None else None

    async def copy_rates_from_pos_df(self, symbol: str, timeframe: int, start_pos: int, count: int) -> pd.DataFrame:
        arr = await self.copy_rates_from_pos(symbol, timeframe, start_pos, count)
        return rates_to_dataframe(arr) if arr is not None else pd.DataFrame()

    async def order_send(self, request: Dict[str, Any]) -> Optional[OrderSendResult]:
        res = await self._rpc_call("order_send", {"request": request})
        return OrderSendResult(**res) if res and isinstance(res, dict) else None

    async def positions_get(self, symbol: str = "", ticket: int = 0) -> Optional[Tuple[TradePosition, ...]]:
        res = await self._rpc_call("positions_get", {"symbol": symbol, "ticket": ticket})
        return tuple(TradePosition(**p) for p in res) if res is not None else None

    async def orders_get(self, symbol: str = "", ticket: int = 0) -> Optional[Tuple[TradeOrder, ...]]:
        res = await self._rpc_call("orders_get", {"symbol": symbol, "ticket": ticket})
        return tuple(TradeOrder(**o) for o in res) if res is not None else None

    async def history_deals_get(self, date_from: Any = None, date_to: Any = None) -> Optional[Tuple[TradeDeal, ...]]:
        res = await self._rpc_call("history_deals_get", {"date_from": date_from, "date_to": date_to})
        return tuple(TradeDeal(**d) for d in res) if res is not None else None
