"""Data types, NamedTuples, and NumPy array converters matching official MetaTrader 5 API."""

from typing import NamedTuple, Optional, List, Dict, Any, Union
import numpy as np
import pandas as pd

# NumPy structured dtype for Rates (OHLCV candles)
RATE_DTYPE = np.dtype([
    ('time', '<i8'),
    ('open', '<f8'),
    ('high', '<f8'),
    ('low', '<f8'),
    ('close', '<f8'),
    ('tick_volume', '<u8'),
    ('spread', '<i4'),
    ('real_volume', '<u8')
])

# NumPy structured dtype for Ticks
TICK_DTYPE = np.dtype([
    ('time', '<i8'),
    ('bid', '<f8'),
    ('ask', '<f8'),
    ('last', '<f8'),
    ('volume', '<u8'),
    ('time_msc', '<i8'),
    ('flags', '<u4'),
    ('volume_real', '<f8')
])


class AccountInfo(NamedTuple):
    """Account information matching official mt5.account_info()."""
    login: int
    trade_mode: int
    leverage: int
    limit_orders: int
    margin_so_mode: int
    trade_allowed: bool
    trade_expert: bool
    margin_mode: int
    currency_digits: int
    fifo_close: bool
    balance: float
    credit: float
    profit: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    margin_so_call: float
    margin_so_so: float
    margin_initial: float
    margin_maintenance: float
    assets: float
    liabilities: float
    commission_blocked: float
    name: str
    server: str
    currency: str
    company: str


class TerminalInfo(NamedTuple):
    """Terminal state information matching official mt5.terminal_info()."""
    community_account: bool
    community_connection: bool
    connected: bool
    dlls_allowed: bool
    trade_allowed: bool
    trade_api_disabled: bool
    email_enabled: bool
    ftp_enabled: bool
    notifications_enabled: bool
    mqid: bool
    build: int
    maxbars: int
    codepage: int
    ping_last: int
    community_balance: float
    retransmission: float
    company: str
    name: str
    language: str
    path: str
    data_path: str
    commondata_path: str


class SymbolInfo(NamedTuple):
    """Symbol specification matching official mt5.symbol_info()."""
    custom: bool
    chart_mode: int
    select: bool
    visible: bool
    session_deals: int
    session_buy_orders: int
    session_sell_orders: int
    volume: int
    volumehigh: int
    volumelow: int
    time: int
    digits: int
    spread: int
    spread_float: bool
    ticks_bookdepth: int
    trade_calc_mode: int
    trade_mode: int
    start_time: int
    expiration_time: int
    trade_stops_level: int
    trade_freeze_level: int
    trade_exemode: int
    swap_mode: int
    swap_rollover3days: int
    margin_hedged_use_leg: bool
    expiration_mode: int
    filling_mode: int
    order_mode: int
    order_gtc_mode: int
    option_mode: int
    option_right: int
    bid: float
    bidhigh: float
    bidlow: float
    ask: float
    askhigh: float
    asklow: float
    last: float
    lasthigh: float
    lastlow: float
    volume_real: float
    volumehigh_real: float
    volumelow_real: float
    option_strike: float
    point: float
    trade_tick_value: float
    trade_tick_value_profit: float
    trade_tick_value_loss: float
    trade_tick_size: float
    trade_contract_size: float
    trade_accrued_interest: float
    trade_face_value: float
    trade_liquidity_rate: float
    volume_min: float
    volume_max: float
    volume_step: float
    volume_limit: float
    swap_long: float
    swap_short: float
    margin_initial: float
    margin_maintenance: float
    session_volume: float
    session_turnover: float
    session_interest: float
    session_buy_orders_volume: float
    session_sell_orders_volume: float
    session_open: float
    session_close: float
    session_aw: float
    session_price_settlement: float
    session_price_limit_min: float
    session_price_limit_max: float
    margin_hedged: float
    price_change: float
    price_volatility: float
    price_theoretical: float
    basis: str
    category: str
    currency_base: str
    currency_profit: str
    currency_margin: str
    bank: str
    description: str
    exchange: str
    formula: str
    isin: str
    name: str
    page: str
    path: str


class Tick(NamedTuple):
    """Price tick matching official mt5.symbol_info_tick()."""
    time: int
    bid: float
    ask: float
    last: float
    volume: int
    time_msc: int
    flags: int
    volume_real: float


class TradeOrder(NamedTuple):
    """Pending or active order matching official mt5.orders_get()."""
    ticket: int
    time_setup: int
    time_setup_msc: int
    time_done: int
    time_done_msc: int
    time_expiration: int
    type: int
    type_time: int
    type_filling: int
    state: int
    magic: int
    position_id: int
    position_by_id: int
    reason: int
    volume_initial: float
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    price_stoplimit: float
    symbol: str
    comment: str
    external_id: str


class TradePosition(NamedTuple):
    """Open position matching official mt5.positions_get()."""
    ticket: int
    time: int
    time_msc: int
    time_update: int
    time_update_msc: int
    type: int
    magic: int
    identifier: int
    reason: int
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float
    profit: float
    symbol: str
    comment: str
    external_id: str


class TradeDeal(NamedTuple):
    """Historical trade deal matching official mt5.history_deals_get()."""
    ticket: int
    order: int
    time: int
    time_msc: int
    type: int
    entry: int
    magic: int
    position_id: int
    reason: int
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    fee: float
    symbol: str
    comment: str
    external_id: str


class OrderSendResult(NamedTuple):
    """Order placement result matching official mt5.order_send()."""
    retcode: int
    deal: int
    order: int
    volume: float
    price: float
    bid: float
    ask: float
    comment: str
    request_id: int
    retcode_external: int
    request: Dict[str, Any]


class OrderCheckResult(NamedTuple):
    """Order validation result matching official mt5.order_check()."""
    retcode: int
    balance: float
    equity: float
    profit: float
    margin: float
    margin_free: float
    margin_level: float
    comment: str
    request: Dict[str, Any]


class BookInfo(NamedTuple):
    """Depth of Market (DOM) entry matching official mt5.market_book_get()."""
    type: int
    price: float
    volume: int
    volume_dbl: float


def rates_to_numpy(rates_list: List[Dict[str, Any]]) -> np.ndarray:
    """Convert list of rate dictionaries to structured NumPy array matching MT5 C-extension."""
    if not rates_list:
        return np.empty(0, dtype=RATE_DTYPE)
    
    arr = np.empty(len(rates_list), dtype=RATE_DTYPE)
    for i, r in enumerate(rates_list):
        arr[i] = (
            int(r.get('time', 0)),
            float(r.get('open', 0.0)),
            float(r.get('high', 0.0)),
            float(r.get('low', 0.0)),
            float(r.get('close', 0.0)),
            int(r.get('tick_volume', 0)),
            int(r.get('spread', 0)),
            int(r.get('real_volume', 0))
        )
    return arr


def ticks_to_numpy(ticks_list: List[Dict[str, Any]]) -> np.ndarray:
    """Convert list of tick dictionaries to structured NumPy array matching MT5 C-extension."""
    if not ticks_list:
        return np.empty(0, dtype=TICK_DTYPE)
        
    arr = np.empty(len(ticks_list), dtype=TICK_DTYPE)
    for i, t in enumerate(ticks_list):
        arr[i] = (
            int(t.get('time', 0)),
            float(t.get('bid', 0.0)),
            float(t.get('ask', 0.0)),
            float(t.get('last', 0.0)),
            int(t.get('volume', 0)),
            int(t.get('time_msc', 0)),
            int(t.get('flags', 0)),
            float(t.get('volume_real', 0.0))
        )
    return arr


def rates_to_dataframe(rates_array_or_list: Union[np.ndarray, List[Dict[str, Any]]]) -> pd.DataFrame:
    """Convert rate structured array or list to pandas DataFrame with datetime index."""
    if isinstance(rates_array_or_list, list):
        arr = rates_to_numpy(rates_array_or_list)
    else:
        arr = rates_array_or_list

    if len(arr) == 0:
        return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'])

    df = pd.DataFrame(arr)
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    return df.set_index('time')
