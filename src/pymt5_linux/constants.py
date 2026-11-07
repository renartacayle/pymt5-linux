"""Constants and Enums matching the official MetaTrader 5 Python API specification.

This module provides 100% binary-compatible integer constants and enums
matching official Windows MetaTrader5 API.
"""

from enum import IntEnum

# ============================================================================
# Timeframes
# ============================================================================
TIMEFRAME_M1 = 1
TIMEFRAME_M2 = 2
TIMEFRAME_M3 = 3
TIMEFRAME_M4 = 4
TIMEFRAME_M5 = 5
TIMEFRAME_M6 = 6
TIMEFRAME_M10 = 10
TIMEFRAME_M12 = 12
TIMEFRAME_M15 = 15
TIMEFRAME_M20 = 20
TIMEFRAME_M30 = 30
TIMEFRAME_H1 = 16385
TIMEFRAME_H2 = 16386
TIMEFRAME_H3 = 16387
TIMEFRAME_H4 = 16388
TIMEFRAME_H6 = 16390
TIMEFRAME_H8 = 16392
TIMEFRAME_H12 = 16396
TIMEFRAME_D1 = 16408
TIMEFRAME_W1 = 32769
TIMEFRAME_MN1 = 49153

class Timeframe(IntEnum):
    M1 = TIMEFRAME_M1
    M2 = TIMEFRAME_M2
    M3 = TIMEFRAME_M3
    M4 = TIMEFRAME_M4
    M5 = TIMEFRAME_M5
    M6 = TIMEFRAME_M6
    M10 = TIMEFRAME_M10
    M12 = TIMEFRAME_M12
    M15 = TIMEFRAME_M15
    M20 = TIMEFRAME_M20
    M30 = TIMEFRAME_M30
    H1 = TIMEFRAME_H1
    H2 = TIMEFRAME_H2
    H3 = TIMEFRAME_H3
    H4 = TIMEFRAME_H4
    H6 = TIMEFRAME_H6
    H8 = TIMEFRAME_H8
    H12 = TIMEFRAME_H12
    D1 = TIMEFRAME_D1
    W1 = TIMEFRAME_W1
    MN1 = TIMEFRAME_MN1

# ============================================================================
# Copy Ticks Flags
# ============================================================================
COPY_TICKS_ALL = -1
COPY_TICKS_INFO = 1
COPY_TICKS_TRADE = 2

# ============================================================================
# Trade Actions (ENUM_TRADE_REQUEST_ACTIONS)
# ============================================================================
TRADE_ACTION_DEAL = 1
TRADE_ACTION_PENDING = 5
TRADE_ACTION_SLTP = 6
TRADE_ACTION_MODIFY = 7
TRADE_ACTION_REMOVE = 8
TRADE_ACTION_CLOSE_BY = 10

class TradeAction(IntEnum):
    DEAL = TRADE_ACTION_DEAL
    PENDING = TRADE_ACTION_PENDING
    SLTP = TRADE_ACTION_SLTP
    MODIFY = TRADE_ACTION_MODIFY
    REMOVE = TRADE_ACTION_REMOVE
    CLOSE_BY = TRADE_ACTION_CLOSE_BY

# ============================================================================
# Order Types (ENUM_ORDER_TYPE)
# ============================================================================
ORDER_TYPE_BUY = 0
ORDER_TYPE_SELL = 1
ORDER_TYPE_BUY_LIMIT = 2
ORDER_TYPE_SELL_LIMIT = 3
ORDER_TYPE_BUY_STOP = 4
ORDER_TYPE_SELL_STOP = 5
ORDER_TYPE_BUY_STOP_LIMIT = 6
ORDER_TYPE_SELL_STOP_LIMIT = 7
ORDER_TYPE_CLOSE_BY = 8

class OrderType(IntEnum):
    BUY = ORDER_TYPE_BUY
    SELL = ORDER_TYPE_SELL
    BUY_LIMIT = ORDER_TYPE_BUY_LIMIT
    SELL_LIMIT = ORDER_TYPE_SELL_LIMIT
    BUY_STOP = ORDER_TYPE_BUY_STOP
    SELL_STOP = ORDER_TYPE_SELL_STOP
    BUY_STOP_LIMIT = ORDER_TYPE_BUY_STOP_LIMIT
    SELL_STOP_LIMIT = ORDER_TYPE_SELL_STOP_LIMIT
    CLOSE_BY = ORDER_TYPE_CLOSE_BY

# ============================================================================
# Order States (ENUM_ORDER_STATE)
# ============================================================================
ORDER_STATE_STARTED = 0
ORDER_STATE_PLACED = 1
ORDER_STATE_CANCELED = 2
ORDER_STATE_PARTIAL = 3
ORDER_STATE_FILLED = 4
ORDER_STATE_REJECTED = 5
ORDER_STATE_EXPIRED = 6
ORDER_STATE_REQUEST_ADD = 7
ORDER_STATE_REQUEST_MODIFY = 8
ORDER_STATE_REQUEST_CANCEL = 9

class OrderState(IntEnum):
    STARTED = ORDER_STATE_STARTED
    PLACED = ORDER_STATE_PLACED
    CANCELED = ORDER_STATE_CANCELED
    PARTIAL = ORDER_STATE_PARTIAL
    FILLED = ORDER_STATE_FILLED
    REJECTED = ORDER_STATE_REJECTED
    EXPIRED = ORDER_STATE_EXPIRED
    REQUEST_ADD = ORDER_STATE_REQUEST_ADD
    REQUEST_MODIFY = ORDER_STATE_REQUEST_MODIFY
    REQUEST_CANCEL = ORDER_STATE_REQUEST_CANCEL

# ============================================================================
# Order Time Expiration (ENUM_ORDER_TYPE_TIME)
# ============================================================================
ORDER_TIME_GTC = 0
ORDER_TIME_DAY = 1
ORDER_TIME_SPECIFIED = 2
ORDER_TIME_SPECIFIED_DAY = 3

class OrderTime(IntEnum):
    GTC = ORDER_TIME_GTC
    DAY = ORDER_TIME_DAY
    SPECIFIED = ORDER_TIME_SPECIFIED
    SPECIFIED_DAY = ORDER_TIME_SPECIFIED_DAY

# ============================================================================
# Order Filling Types (ENUM_ORDER_TYPE_FILLING)
# ============================================================================
ORDER_FILLING_FOK = 0
ORDER_FILLING_IOC = 1
ORDER_FILLING_RETURN = 2
ORDER_FILLING_BOC = 3

class OrderFilling(IntEnum):
    FOK = ORDER_FILLING_FOK
    IOC = ORDER_FILLING_IOC
    RETURN = ORDER_FILLING_RETURN
    BOC = ORDER_FILLING_BOC

# ============================================================================
# Position Types (ENUM_POSITION_TYPE)
# ============================================================================
POSITION_TYPE_BUY = 0
POSITION_TYPE_SELL = 1

class PositionType(IntEnum):
    BUY = POSITION_TYPE_BUY
    SELL = POSITION_TYPE_SELL

# ============================================================================
# Position Reasons (ENUM_POSITION_REASON)
# ============================================================================
POSITION_REASON_CLIENT = 0
POSITION_REASON_MOBILE = 1
POSITION_REASON_WEB = 2
POSITION_REASON_EXPERT = 3

# ============================================================================
# Deal Types (ENUM_DEAL_TYPE)
# ============================================================================
DEAL_TYPE_BUY = 0
DEAL_TYPE_SELL = 1
DEAL_TYPE_BALANCE = 2
DEAL_TYPE_CREDIT = 3
DEAL_TYPE_CHARGE = 4
DEAL_TYPE_CORRECTION = 5
DEAL_TYPE_BONUS = 6
DEAL_TYPE_COMMISSION = 7
DEAL_TYPE_COMMISSION_DAILY = 8
DEAL_TYPE_COMMISSION_MONTHLY = 9
DEAL_TYPE_COMMISSION_AGENT_DAILY = 10
DEAL_TYPE_COMMISSION_AGENT_MONTHLY = 11
DEAL_TYPE_INTEREST = 12
DEAL_TYPE_BUY_CANCELED = 13
DEAL_TYPE_SELL_CANCELED = 14
DEAL_DIVIDEND = 15
DEAL_DIVIDEND_FRANKED = 16
DEAL_TAX = 17

# ============================================================================
# Deal Entry (ENUM_DEAL_ENTRY)
# ============================================================================
DEAL_ENTRY_IN = 0
DEAL_ENTRY_OUT = 1
DEAL_ENTRY_INOUT = 2
DEAL_ENTRY_OUT_BY = 3

# ============================================================================
# Deal Reason (ENUM_DEAL_REASON)
# ============================================================================
DEAL_REASON_CLIENT = 0
DEAL_REASON_MOBILE = 1
DEAL_REASON_WEB = 2
DEAL_REASON_EXPERT = 3
DEAL_REASON_SL = 4
DEAL_REASON_TP = 5
DEAL_REASON_SO = 6
DEAL_REASON_ROLLOVER = 7
DEAL_REASON_VMARGIN = 8
DEAL_REASON_SPLIT = 9

# ============================================================================
# Market Book Types (ENUM_BOOK_TYPE)
# ============================================================================
BOOK_TYPE_SELL = 1
BOOK_TYPE_BUY = 2
BOOK_TYPE_SELL_MARKET = 3
BOOK_TYPE_BUY_MARKET = 4

# ============================================================================
# Account Trade Mode (ENUM_ACCOUNT_TRADE_MODE)
# ============================================================================
ACCOUNT_TRADE_MODE_DEMO = 0
ACCOUNT_TRADE_MODE_CONTEST = 1
ACCOUNT_TRADE_MODE_REAL = 2

# ============================================================================
# Account Margin Mode (ENUM_ACCOUNT_MARGIN_MODE)
# ============================================================================
ACCOUNT_MARGIN_MODE_RETAIL_NETTING = 0
ACCOUNT_MARGIN_MODE_EXCHANGE = 1
ACCOUNT_MARGIN_MODE_RETAIL_HEDGING = 2

# ============================================================================
# Trade Return Codes (Trade Retcodes)
# ============================================================================
TRADE_RETCODE_REQUOTE = 10004
TRADE_RETCODE_REJECT = 10006
TRADE_RETCODE_CANCEL = 10007
TRADE_RETCODE_PLACED = 10008
TRADE_RETCODE_DONE = 10009
TRADE_RETCODE_DONE_PARTIAL = 10010
TRADE_RETCODE_ERROR = 10011
TRADE_RETCODE_TIMEOUT = 10012
TRADE_RETCODE_INVALID = 10013
TRADE_RETCODE_INVALID_VOLUME = 10014
TRADE_RETCODE_INVALID_PRICE = 10015
TRADE_RETCODE_INVALID_STOPS = 10016
TRADE_RETCODE_TRADE_DISABLED = 10017
TRADE_RETCODE_MARKET_CLOSED = 10018
TRADE_RETCODE_NO_MONEY = 10019
TRADE_RETCODE_PRICE_CHANGED = 10020
TRADE_RETCODE_PRICE_OFF = 10021
TRADE_RETCODE_INVALID_EXPIRATION = 10022
TRADE_RETCODE_ORDER_CHANGED = 10023
TRADE_RETCODE_TOO_MANY_REQUESTS = 10024
TRADE_RETCODE_NO_CHANGES = 10025
TRADE_RETCODE_SERVER_DISABLES_AT = 10026
TRADE_RETCODE_CLIENT_DISABLES_AT = 10027
TRADE_RETCODE_LOCKED = 10028
TRADE_RETCODE_FROZEN = 10029
TRADE_RETCODE_INVALID_FILL = 10030
TRADE_RETCODE_CONNECTION = 10031
TRADE_RETCODE_ONLY_REAL = 10032
TRADE_RETCODE_LIMIT_ORDERS = 10033
TRADE_RETCODE_LIMIT_VOLUME = 10034
TRADE_RETCODE_INVALID_ORDER = 10035
TRADE_RETCODE_POSITION_CLOSED = 10036
TRADE_RETCODE_INVALID_CLOSE_VOLUME = 10038
TRADE_RETCODE_CLOSE_ORDER_EXIST = 10039
TRADE_RETCODE_LIMIT_POSITIONS = 10040

# Symbol chart modes
SYMBOL_CHART_MODE_BID = 0
SYMBOL_CHART_MODE_LAST = 1

# Symbol calc modes
SYMBOL_CALC_MODE_FOREX = 0
SYMBOL_CALC_MODE_FUTURES = 1
SYMBOL_CALC_MODE_CFD = 2
SYMBOL_CALC_MODE_CFDINDEX = 3
SYMBOL_CALC_MODE_CFDLEVERAGE = 4
SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE = 5
SYMBOL_CALC_MODE_EXCH_STOCKS = 32
SYMBOL_CALC_MODE_EXCH_FUTURES = 33
SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS = 34
SYMBOL_CALC_MODE_EXCH_BONDS = 35
SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX = 36
SYMBOL_CALC_MODE_EXCH_BONDS_MOEX = 37
SYMBOL_CALC_MODE_SERV_COLLATERAL = 64
