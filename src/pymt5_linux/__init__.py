"""pymt5-linux: Production-grade MetaTrader 5 SDK and Drop-in Replacement for Linux.

Enables algorithmic and AI trading bots on Linux via high-speed Wine IPC bridge,
remote VPS gateway, standalone simulator, and asynchronous streaming.
"""

from ._version import __version__, __author__

# Constants & Enums
from .constants import (
    TIMEFRAME_M1, TIMEFRAME_M2, TIMEFRAME_M3, TIMEFRAME_M4, TIMEFRAME_M5,
    TIMEFRAME_M6, TIMEFRAME_M10, TIMEFRAME_M12, TIMEFRAME_M15, TIMEFRAME_M20,
    TIMEFRAME_M30, TIMEFRAME_H1, TIMEFRAME_H2, TIMEFRAME_H3, TIMEFRAME_H4,
    TIMEFRAME_H6, TIMEFRAME_H8, TIMEFRAME_H12, TIMEFRAME_D1, TIMEFRAME_W1,
    TIMEFRAME_MN1, Timeframe,
    COPY_TICKS_ALL, COPY_TICKS_INFO, COPY_TICKS_TRADE,
    TRADE_ACTION_DEAL, TRADE_ACTION_PENDING, TRADE_ACTION_SLTP,
    TRADE_ACTION_MODIFY, TRADE_ACTION_REMOVE, TRADE_ACTION_CLOSE_BY, TradeAction,
    ORDER_TYPE_BUY, ORDER_TYPE_SELL, ORDER_TYPE_BUY_LIMIT, ORDER_TYPE_SELL_LIMIT,
    ORDER_TYPE_BUY_STOP, ORDER_TYPE_SELL_STOP, ORDER_TYPE_BUY_STOP_LIMIT,
    ORDER_TYPE_SELL_STOP_LIMIT, ORDER_TYPE_CLOSE_BY, OrderType,
    ORDER_STATE_STARTED, ORDER_STATE_PLACED, ORDER_STATE_CANCELED,
    ORDER_STATE_PARTIAL, ORDER_STATE_FILLED, ORDER_STATE_REJECTED,
    ORDER_STATE_EXPIRED, ORDER_STATE_REQUEST_ADD, ORDER_STATE_REQUEST_MODIFY,
    ORDER_STATE_REQUEST_CANCEL, OrderState,
    ORDER_TIME_GTC, ORDER_TIME_DAY, ORDER_TIME_SPECIFIED, ORDER_TIME_SPECIFIED_DAY, OrderTime,
    ORDER_FILLING_FOK, ORDER_FILLING_IOC, ORDER_FILLING_RETURN, ORDER_FILLING_BOC, OrderFilling,
    POSITION_TYPE_BUY, POSITION_TYPE_SELL, PositionType,
    POSITION_REASON_CLIENT, POSITION_REASON_MOBILE, POSITION_REASON_WEB, POSITION_REASON_EXPERT,
    DEAL_TYPE_BUY, DEAL_TYPE_SELL, DEAL_TYPE_BALANCE, DEAL_TYPE_CREDIT,
    DEAL_TYPE_CHARGE, DEAL_TYPE_CORRECTION, DEAL_TYPE_BONUS, DEAL_TYPE_COMMISSION,
    DEAL_TYPE_COMMISSION_DAILY, DEAL_TYPE_COMMISSION_MONTHLY,
    DEAL_TYPE_COMMISSION_AGENT_DAILY, DEAL_TYPE_COMMISSION_AGENT_MONTHLY,
    DEAL_TYPE_INTEREST, DEAL_TYPE_BUY_CANCELED, DEAL_TYPE_SELL_CANCELED,
    DEAL_DIVIDEND, DEAL_DIVIDEND_FRANKED, DEAL_TAX,
    DEAL_ENTRY_IN, DEAL_ENTRY_OUT, DEAL_ENTRY_INOUT, DEAL_ENTRY_OUT_BY,
    DEAL_REASON_CLIENT, DEAL_REASON_MOBILE, DEAL_REASON_WEB, DEAL_REASON_EXPERT,
    DEAL_REASON_SL, DEAL_REASON_TP, DEAL_REASON_SO, DEAL_REASON_ROLLOVER,
    DEAL_REASON_VMARGIN, DEAL_REASON_SPLIT,
    BOOK_TYPE_SELL, BOOK_TYPE_BUY, BOOK_TYPE_SELL_MARKET, BOOK_TYPE_BUY_MARKET,
    ACCOUNT_TRADE_MODE_DEMO, ACCOUNT_TRADE_MODE_CONTEST, ACCOUNT_TRADE_MODE_REAL,
    ACCOUNT_MARGIN_MODE_RETAIL_NETTING, ACCOUNT_MARGIN_MODE_EXCHANGE, ACCOUNT_MARGIN_MODE_RETAIL_HEDGING,
    TRADE_RETCODE_REQUOTE, TRADE_RETCODE_REJECT, TRADE_RETCODE_CANCEL,
    TRADE_RETCODE_PLACED, TRADE_RETCODE_DONE, TRADE_RETCODE_DONE_PARTIAL,
    TRADE_RETCODE_ERROR, TRADE_RETCODE_TIMEOUT, TRADE_RETCODE_INVALID,
    TRADE_RETCODE_INVALID_VOLUME, TRADE_RETCODE_INVALID_PRICE, TRADE_RETCODE_INVALID_STOPS,
    TRADE_RETCODE_TRADE_DISABLED, TRADE_RETCODE_MARKET_CLOSED, TRADE_RETCODE_NO_MONEY,
    TRADE_RETCODE_PRICE_CHANGED, TRADE_RETCODE_PRICE_OFF, TRADE_RETCODE_INVALID_EXPIRATION,
    TRADE_RETCODE_ORDER_CHANGED, TRADE_RETCODE_TOO_MANY_REQUESTS, TRADE_RETCODE_NO_CHANGES,
    TRADE_RETCODE_SERVER_DISABLES_AT, TRADE_RETCODE_CLIENT_DISABLES_AT, TRADE_RETCODE_LOCKED,
    TRADE_RETCODE_FROZEN, TRADE_RETCODE_INVALID_FILL, TRADE_RETCODE_CONNECTION,
    TRADE_RETCODE_ONLY_REAL, TRADE_RETCODE_LIMIT_ORDERS, TRADE_RETCODE_LIMIT_VOLUME,
    TRADE_RETCODE_INVALID_ORDER, TRADE_RETCODE_POSITION_CLOSED, TRADE_RETCODE_INVALID_CLOSE_VOLUME,
    TRADE_RETCODE_CLOSE_ORDER_EXIST, TRADE_RETCODE_LIMIT_POSITIONS
)

# Errors & Exceptions
from .errors import (
    RES_S_OK, RES_E_FAIL, RES_E_INVALID_PARAMS, RES_E_NO_MEMORY,
    RES_E_NOT_FOUND, RES_E_INVALID_VERSION, RES_E_AUTH_FAILED,
    RES_E_UNSUPPORTED, RES_E_AUTO_TRADING_DISABLED, RES_E_INTERNAL_FAIL,
    RES_E_INTERNAL_FAIL_SEND, RES_E_INTERNAL_FAIL_RECEIVE,
    RES_E_INTERNAL_FAIL_INIT, RES_E_INTERNAL_FAIL_CONNECT,
    RES_E_INTERNAL_FAIL_TIMEOUT, MT5Error, MT5ConnectionError, MT5TimeoutError
)

# Data Structures & NamedTuples
from .types import (
    AccountInfo, TerminalInfo, SymbolInfo, Tick, TradeOrder,
    TradePosition, TradeDeal, OrderSendResult, OrderCheckResult, BookInfo,
    RATE_DTYPE, TICK_DTYPE, rates_to_numpy, ticks_to_numpy, rates_to_dataframe
)

# Clients & Engines
from .client import (
    MetaTrader5Client, default_client,
    initialize, shutdown, version, terminal_info, account_info, login,
    symbols_total, symbols_get, symbol_info, symbol_info_tick, symbol_select,
    copy_rates_from, copy_rates_from_pos, copy_rates_from_pos_df,
    copy_rates_range, copy_ticks_from,
    order_send, order_check, order_calc_margin, order_calc_profit,
    orders_total, orders_get, positions_total, positions_get,
    history_orders_total, history_orders_get, history_deals_total,
    history_deals_get, last_error
)
from .async_client import AsyncMetaTrader5
from .streaming import MT5Streamer
from .gateway import MT5GatewayServer
from .mock_engine import MockMT5Engine

# Alias for drop-in replacement (`from pymt5_linux import MetaTrader5 as mt5`)
MetaTrader5 = default_client

__all__ = [
    "__version__", "__author__",
    "MetaTrader5", "MetaTrader5Client", "AsyncMetaTrader5", "MT5Streamer",
    "MT5GatewayServer", "MockMT5Engine",
    # Functions
    "initialize", "shutdown", "version", "terminal_info", "account_info", "login",
    "symbols_total", "symbols_get", "symbol_info", "symbol_info_tick", "symbol_select",
    "copy_rates_from", "copy_rates_from_pos", "copy_rates_from_pos_df",
    "copy_rates_range", "copy_ticks_from",
    "order_send", "order_check", "order_calc_margin", "order_calc_profit",
    "orders_total", "orders_get", "positions_total", "positions_get",
    "history_orders_total", "history_orders_get", "history_deals_total",
    "history_deals_get", "last_error",
    # Types
    "AccountInfo", "TerminalInfo", "SymbolInfo", "Tick", "TradeOrder",
    "TradePosition", "TradeDeal", "OrderSendResult", "OrderCheckResult", "BookInfo",
    "RATE_DTYPE", "TICK_DTYPE", "rates_to_numpy", "ticks_to_numpy", "rates_to_dataframe",
    # Errors
    "RES_S_OK", "RES_E_FAIL", "MT5Error", "MT5ConnectionError", "MT5TimeoutError"
]
