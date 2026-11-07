"""Synchronous 1:1 drop-in replacement client for official MetaTrader 5 API on Linux."""

import socket
import uuid
import datetime
import logging
from typing import Optional, Tuple, Union, List, Dict, Any
import numpy as np
import pandas as pd

from .protocol import send_packet, receive_packet
from .constants import (
    TIMEFRAME_M1,
    ORDER_TYPE_BUY,
    TRADE_RETCODE_DONE,
    TRADE_RETCODE_ERROR,
    COPY_TICKS_ALL
)
from .errors import (
    RES_S_OK,
    RES_E_FAIL,
    RES_E_NOT_FOUND,
    RES_E_INTERNAL_FAIL_CONNECT,
    format_error
)
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
    BookInfo,
    rates_to_numpy,
    ticks_to_numpy,
    rates_to_dataframe
)
from .gateway import MT5GatewayServer

logger = logging.getLogger("pymt5_linux.client")


class MetaTrader5Client:
    """Drop-in MetaTrader 5 client implementing official C-API signatures."""

    def __init__(self) -> None:
        self.host: str = "127.0.0.1"
        self.port: int = 18812
        self.sock: Optional[socket.socket] = None
        self._last_err: Tuple[int, str] = (RES_S_OK, "Success")
        self._connected: bool = False
        self._internal_server: Optional[MT5GatewayServer] = None

    def last_error(self) -> Tuple[int, str]:
        """Return the last error as (code, description)."""
        return self._last_err

    def _set_error(self, code: int, msg: str = "") -> None:
        self._last_err = format_error(code, msg)

    def _rpc_call(self, method: str, params: Any = None) -> Any:
        """Execute a synchronized Remote Procedure Call to the gateway."""
        if not self._connected or not self.sock:
            self._set_error(RES_E_INTERNAL_FAIL_CONNECT, "Client is not connected to MT5 gateway")
            return None

        req_id = str(uuid.uuid4())
        packet = {"id": req_id, "method": method, "params": params or {}}

        try:
            send_packet(self.sock, packet)
            response = receive_packet(self.sock, timeout=30.0)
            if response.get("error"):
                err = response["error"]
                self._set_error(err.get("code", RES_E_FAIL), err.get("message", "RPC Error"))
                return None
            self._set_error(RES_S_OK, "Success")
            return response.get("result")
        except socket.timeout:
            self._set_error(RES_E_FAIL, f"RPC call '{method}' timed out")
            return None
        except Exception as e:
            self._set_error(RES_E_INTERNAL_FAIL_CONNECT, f"Communication error: {e}")
            self._connected = False
            return None

    def initialize(
        self,
        path: str = "",
        login: int = 0,
        server: str = "",
        password: str = "",
        timeout: int = 60000,
        portable: bool = False,
        host: str = "127.0.0.1",
        port: int = 18812,
        auto_start_mock: bool = True
    ) -> bool:
        """Initialize connection to MetaTrader 5 terminal or Wine gateway."""
        self.host = host
        self.port = port

        # Connect to existing running gateway
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5.0)
            self.sock.connect((self.host, self.port))
            self._connected = True
        except (ConnectionRefusedError, OSError):
            if auto_start_mock:
                logger.info(f"No existing gateway found on {host}:{port}. Spawning embedded Mock Gateway...")
                self._internal_server = MT5GatewayServer(host=self.host, port=self.port, force_mock=True)
                self._internal_server.start(blocking=False)
                
                # Retry connection
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(5.0)
                self.sock.connect((self.host, self.port))
                self._connected = True
            else:
                self._set_error(RES_E_INTERNAL_FAIL_CONNECT, f"Failed connecting to {host}:{port}")
                return False

        res = self._rpc_call("initialize", {
            "path": path, "login": login, "server": server,
            "password": password, "timeout": timeout, "portable": portable
        })
        return bool(res)

    def shutdown(self) -> None:
        """Close connection to terminal and release resources."""
        if self._connected and self.sock:
            try:
                self._rpc_call("shutdown")
            except Exception:
                pass
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            self._connected = False

        if self._internal_server:
            self._internal_server.stop()
            self._internal_server = None

    def version(self) -> Optional[Tuple[int, int, str]]:
        """Get MetaTrader 5 version (terminal_version, build, build_date)."""
        res = self._rpc_call("version")
        if isinstance(res, (list, tuple)) and len(res) >= 3:
            return (res[0], res[1], res[2])
        return None

    def terminal_info(self) -> Optional[TerminalInfo]:
        """Get terminal parameters and state."""
        res = self._rpc_call("terminal_info")
        if not res or not isinstance(res, dict):
            return None
        return TerminalInfo(**res)

    def account_info(self) -> Optional[AccountInfo]:
        """Get live trading account information."""
        res = self._rpc_call("account_info")
        if not res or not isinstance(res, dict):
            return None
        return AccountInfo(**res)

    def login(self, login: int, password: str = "", server: str = "", timeout: int = 60000) -> bool:
        """Connect to a trading account with login and server credentials."""
        res = self._rpc_call("login", {
            "login": login, "password": password, "server": server, "timeout": timeout
        })
        return bool(res)

    def symbols_total(self) -> int:
        """Get total number of financial instruments available."""
        res = self._rpc_call("symbols_total")
        return int(res or 0)

    def symbol_select(self, symbol: str, enable: bool = True) -> bool:
        """Select a symbol in the Market Watch window or remove a symbol from the window."""
        res = self._rpc_call("symbol_select", {"symbol": symbol, "enable": enable})
        return bool(res)

    def symbols_get(self, group: str = "") -> Optional[Tuple[SymbolInfo, ...]]:
        """Get all symbols or symbols matching group filter."""
        res = self._rpc_call("symbols_get", {"group": group})
        if res is None:
            return None
        return tuple(SymbolInfo(**s) for s in res)

    def symbol_info(self, symbol: str) -> Optional[SymbolInfo]:
        """Get properties of the specified symbol."""
        res = self._rpc_call("symbol_info", {"symbol": symbol})
        if not res or not isinstance(res, dict):
            return None
        return SymbolInfo(**res)

    def symbol_info_tick(self, symbol: str) -> Optional[Tick]:
        """Get the last tick for a specified financial instrument."""
        res = self._rpc_call("symbol_info_tick", {"symbol": symbol})
        if not res or not isinstance(res, dict):
            return None
        return Tick(**res)

    def copy_rates_from_pos(self, symbol: str, timeframe: int, start_pos: int, count: int) -> Optional[np.ndarray]:
        """Get historical bars starting from start_pos as structured numpy array."""
        res = self._rpc_call("copy_rates_from_pos", {
            "symbol": symbol, "timeframe": timeframe,
            "start_pos": start_pos, "count": count
        })
        if res is None:
            return None
        return rates_to_numpy(res)

    def copy_rates_from_pos_df(self, symbol: str, timeframe: int, start_pos: int, count: int) -> pd.DataFrame:
        """Get historical bars starting from start_pos converted directly to pandas DataFrame."""
        arr = self.copy_rates_from_pos(symbol, timeframe, start_pos, count)
        if arr is None:
            return pd.DataFrame()
        return rates_to_dataframe(arr)

    def copy_rates_from(self, symbol: str, timeframe: int, date_from: Any, count: int) -> Optional[np.ndarray]:
        """Get historical bars starting from a specific date."""
        if isinstance(date_from, (datetime.datetime, datetime.date)):
            date_from = int(date_from.timestamp())
        res = self._rpc_call("copy_rates_from", {
            "symbol": symbol, "timeframe": timeframe,
            "date_from": date_from, "count": count
        })
        if res is None:
            return None
        return rates_to_numpy(res)

    def copy_rates_range(self, symbol: str, timeframe: int, date_from: Any, date_to: Any) -> Optional[np.ndarray]:
        """Get bars in the specified date range."""
        if isinstance(date_from, (datetime.datetime, datetime.date)):
            date_from = int(date_from.timestamp())
        if isinstance(date_to, (datetime.datetime, datetime.date)):
            date_to = int(date_to.timestamp())
        res = self._rpc_call("copy_rates_range", {
            "symbol": symbol, "timeframe": timeframe,
            "date_from": date_from, "date_to": date_to
        })
        if res is None:
            return None
        return rates_to_numpy(res)

    def copy_ticks_from(self, symbol: str, date_from: Any, count: int, flags: int = COPY_TICKS_ALL) -> Optional[np.ndarray]:
        """Get ticks from a specified date."""
        if isinstance(date_from, (datetime.datetime, datetime.date)):
            date_from = int(date_from.timestamp())
        res = self._rpc_call("copy_ticks_from", {
            "symbol": symbol, "date_from": date_from,
            "count": count, "flags": flags
        })
        if res is None:
            return None
        return ticks_to_numpy(res)

    def order_send(self, request: Dict[str, Any]) -> Optional[OrderSendResult]:
        """Send a trade request to execute or place an order."""
        res = self._rpc_call("order_send", {"request": request})
        if not res or not isinstance(res, dict):
            return None
        return OrderSendResult(**res)

    def order_check(self, request: Dict[str, Any]) -> Optional[OrderCheckResult]:
        """Check margin sufficiency and validate trade request before sending."""
        res = self._rpc_call("order_check", {"request": request})
        if not res or not isinstance(res, dict):
            return None
        return OrderCheckResult(**res)

    def order_calc_margin(self, action: int, symbol: str, volume: float, price: float) -> Optional[float]:
        """Calculate required margin for an order."""
        return self._rpc_call("order_calc_margin", {
            "action": action, "symbol": symbol, "volume": volume, "price": price
        })

    def order_calc_profit(self, action: int, symbol: str, volume: float, price_open: float, price_close: float) -> Optional[float]:
        """Calculate estimated profit for a trade."""
        return self._rpc_call("order_calc_profit", {
            "action": action, "symbol": symbol, "volume": volume,
            "price_open": price_open, "price_close": price_close
        })

    def orders_total(self) -> int:
        """Get total active pending orders."""
        res = self._rpc_call("orders_total")
        return int(res or 0)

    def orders_get(self, symbol: str = "", ticket: int = 0, group: str = "") -> Optional[Tuple[TradeOrder, ...]]:
        """Get active pending orders with optional filtering."""
        res = self._rpc_call("orders_get", {"symbol": symbol, "ticket": ticket, "group": group})
        if res is None:
            return None
        return tuple(TradeOrder(**o) for o in res)

    def positions_total(self) -> int:
        """Get total count of currently open positions."""
        res = self._rpc_call("positions_total")
        return int(res or 0)

    def positions_get(self, symbol: str = "", ticket: int = 0, group: str = "") -> Optional[Tuple[TradePosition, ...]]:
        """Get open positions with optional filtering."""
        res = self._rpc_call("positions_get", {"symbol": symbol, "ticket": ticket, "group": group})
        if res is None:
            return None
        return tuple(TradePosition(**p) for p in res)

    def history_orders_total(self, date_from: Any = None, date_to: Any = None) -> int:
        """Get total number of historical orders."""
        res = self._rpc_call("history_orders_total", {"date_from": date_from, "date_to": date_to})
        return int(res or 0)

    def history_orders_get(self, date_from: Any = None, date_to: Any = None, group: str = "", ticket: int = 0, position: int = 0) -> Optional[Tuple[TradeOrder, ...]]:
        """Get historical orders matching filter criteria."""
        res = self._rpc_call("history_orders_get", {
            "date_from": date_from, "date_to": date_to,
            "group": group, "ticket": ticket, "position": position
        })
        if res is None:
            return None
        return tuple(TradeOrder(**o) for o in res)

    def history_deals_total(self, date_from: Any = None, date_to: Any = None) -> int:
        """Get total number of deals in history."""
        res = self._rpc_call("history_deals_total", {"date_from": date_from, "date_to": date_to})
        return int(res or 0)

    def history_deals_get(self, date_from: Any = None, date_to: Any = None, group: str = "", ticket: int = 0, position: int = 0) -> Optional[Tuple[TradeDeal, ...]]:
        """Get deals from trading history."""
        res = self._rpc_call("history_deals_get", {
            "date_from": date_from, "date_to": date_to,
            "group": group, "ticket": ticket, "position": position
        })
        if res is None:
            return None
        return tuple(TradeDeal(**d) for d in res)


# Global singleton instance for 1:1 drop-in replacement (`import pymt5_linux as mt5`)
default_client = MetaTrader5Client()

# Export functions matching official module level mt5.*
initialize = default_client.initialize
shutdown = default_client.shutdown
version = default_client.version
terminal_info = default_client.terminal_info
account_info = default_client.account_info
login = default_client.login
symbols_total = default_client.symbols_total
symbol_select = default_client.symbol_select
symbols_get = default_client.symbols_get
symbol_info = default_client.symbol_info
symbol_info_tick = default_client.symbol_info_tick
copy_rates_from = default_client.copy_rates_from
copy_rates_from_pos = default_client.copy_rates_from_pos
copy_rates_from_pos_df = default_client.copy_rates_from_pos_df
copy_rates_range = default_client.copy_rates_range
copy_ticks_from = default_client.copy_ticks_from
order_send = default_client.order_send
order_check = default_client.order_check
order_calc_margin = default_client.order_calc_margin
order_calc_profit = default_client.order_calc_profit
orders_total = default_client.orders_total
orders_get = default_client.orders_get
positions_total = default_client.positions_total
positions_get = default_client.positions_get
history_orders_total = default_client.history_orders_total
history_orders_get = default_client.history_orders_get
history_deals_total = default_client.history_deals_total
history_deals_get = default_client.history_deals_get
last_error = default_client.last_error
