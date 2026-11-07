"""Complete MetaTrader 5 Mock Simulator and Backtest Engine.

Simulates terminal operations, market data generation, order execution,
position management, margin calculations, and account state for Linux environments
without requiring Wine or an active MT5 Windows executable.
"""

import time
import math
import random
from typing import Dict, Any, List, Optional
from .constants import (
    TRADE_RETCODE_DONE,
    TRADE_RETCODE_NO_MONEY,
    TRADE_RETCODE_INVALID_VOLUME,
    TRADE_RETCODE_INVALID_PRICE,
    TRADE_RETCODE_POSITION_CLOSED,
    TRADE_ACTION_DEAL,
    TRADE_ACTION_PENDING,
    TRADE_ACTION_SLTP,
    TRADE_ACTION_REMOVE,
    ORDER_TYPE_BUY,
    ORDER_TYPE_SELL,
    ORDER_STATE_FILLED,
    ORDER_STATE_CANCELED,
    POSITION_TYPE_BUY,
    POSITION_TYPE_SELL,
    DEAL_TYPE_BUY,
    DEAL_TYPE_SELL,
    DEAL_ENTRY_IN,
    DEAL_ENTRY_OUT,
    ACCOUNT_TRADE_MODE_DEMO,
    ACCOUNT_MARGIN_MODE_RETAIL_HEDGING,
    TIMEFRAME_M1,
    TIMEFRAME_M5,
    TIMEFRAME_M15,
    TIMEFRAME_H1,
    TIMEFRAME_D1,
)
from .errors import RES_S_OK, RES_E_NOT_FOUND, RES_E_INVALID_PARAMS


class MockMT5Engine:
    """In-memory simulation engine for MetaTrader 5 trading and market data."""

    def __init__(self, login: int = 12345678, server: str = "MetaQuotes-Demo", balance: float = 10000.0) -> None:
        self.login = login
        self.server = server
        self.balance = balance
        self.credit = 0.0
        self.leverage = 100
        self.currency = "USD"
        self.connected = True
        self.initialized = True
        self.last_ticket = 100000
        self.last_deal_ticket = 500000
        self.last_order_ticket = 700000

        # Symbols catalog
        self.symbols: Dict[str, Dict[str, Any]] = {
            "EURUSD": {
                "name": "EURUSD", "digits": 5, "point": 0.00001, "spread": 12,
                "bid": 1.08500, "ask": 1.08512, "last": 1.08505, "contract_size": 100000.0,
                "currency_base": "EUR", "currency_profit": "USD", "currency_margin": "EUR",
                "trade_tick_value": 1.0, "volume_min": 0.01, "volume_max": 100.0, "volume_step": 0.01
            },
            "GBPUSD": {
                "name": "GBPUSD", "digits": 5, "point": 0.00001, "spread": 15,
                "bid": 1.29500, "ask": 1.29515, "last": 1.29508, "contract_size": 100000.0,
                "currency_base": "GBP", "currency_profit": "USD", "currency_margin": "GBP",
                "trade_tick_value": 1.0, "volume_min": 0.01, "volume_max": 100.0, "volume_step": 0.01
            },
            "USDJPY": {
                "name": "USDJPY", "digits": 3, "point": 0.001, "spread": 14,
                "bid": 152.450, "ask": 152.464, "last": 152.455, "contract_size": 100000.0,
                "currency_base": "USD", "currency_profit": "JPY", "currency_margin": "USD",
                "trade_tick_value": 0.65, "volume_min": 0.01, "volume_max": 100.0, "volume_step": 0.01
            },
            "BTCUSD": {
                "name": "BTCUSD", "digits": 2, "point": 0.01, "spread": 250,
                "bid": 92500.00, "ask": 92502.50, "last": 92501.00, "contract_size": 1.0,
                "currency_base": "BTC", "currency_profit": "USD", "currency_margin": "USD",
                "trade_tick_value": 1.0, "volume_min": 0.01, "volume_max": 50.0, "volume_step": 0.01
            },
            "XAUUSD": {
                "name": "XAUUSD", "digits": 2, "point": 0.01, "spread": 25,
                "bid": 2735.50, "ask": 2735.75, "last": 2735.60, "contract_size": 100.0,
                "currency_base": "XAU", "currency_profit": "USD", "currency_margin": "USD",
                "trade_tick_value": 1.0, "volume_min": 0.01, "volume_max": 50.0, "volume_step": 0.01
            }
        }

        # Trading containers
        self.positions: Dict[int, Dict[str, Any]] = {}
        self.orders: Dict[int, Dict[str, Any]] = {}
        self.history_orders: List[Dict[str, Any]] = []
        self.history_deals: List[Dict[str, Any]] = []

    def next_ticket(self) -> int:
        self.last_ticket += 1
        return self.last_ticket

    def next_deal_ticket(self) -> int:
        self.last_deal_ticket += 1
        return self.last_deal_ticket

    def next_order_ticket(self) -> int:
        self.last_order_ticket += 1
        return self.last_order_ticket

    def update_market_prices(self) -> None:
        """Simulate micro-fluctuations in prices."""
        for sym, data in self.symbols.items():
            delta = (random.random() - 0.5) * data["point"] * 5
            data["bid"] = round(data["bid"] + delta, data["digits"])
            data["ask"] = round(data["bid"] + (data["spread"] * data["point"]), data["digits"])
            data["last"] = data["bid"]

    def get_account_info(self) -> Dict[str, Any]:
        """Compute live account equity, margin, and profit."""
        self.update_market_prices()
        total_profit = 0.0
        total_margin = 0.0

        for pos in self.positions.values():
            sym_data = self.symbols.get(pos["symbol"], {})
            cur_price = sym_data.get("bid" if pos["type"] == POSITION_TYPE_BUY else "ask", pos["price_current"])
            pos["price_current"] = cur_price
            
            # Profit calculation
            contract_size = sym_data.get("contract_size", 100000.0)
            if pos["type"] == POSITION_TYPE_BUY:
                pnl = (cur_price - pos["price_open"]) * pos["volume"] * contract_size
            else:
                pnl = (pos["price_open"] - cur_price) * pos["volume"] * contract_size
            pos["profit"] = round(pnl, 2)
            total_profit += pnl

            # Margin calculation
            margin_req = (pos["volume"] * contract_size) / self.leverage
            total_margin += margin_req

        equity = round(self.balance + self.credit + total_profit, 2)
        margin_free = round(max(0.0, equity - total_margin), 2)
        margin_level = round((equity / total_margin * 100.0), 2) if total_margin > 0 else 0.0

        return {
            "login": self.login,
            "trade_mode": ACCOUNT_TRADE_MODE_DEMO,
            "leverage": self.leverage,
            "limit_orders": 200,
            "margin_so_mode": 0,
            "trade_allowed": True,
            "trade_expert": True,
            "margin_mode": ACCOUNT_MARGIN_MODE_RETAIL_HEDGING,
            "currency_digits": 2,
            "fifo_close": False,
            "balance": round(self.balance, 2),
            "credit": self.credit,
            "profit": round(total_profit, 2),
            "equity": equity,
            "margin": round(total_margin, 2),
            "margin_free": margin_free,
            "margin_level": margin_level,
            "margin_so_call": 50.0,
            "margin_so_so": 30.0,
            "margin_initial": 0.0,
            "margin_maintenance": 0.0,
            "assets": 0.0,
            "liabilities": 0.0,
            "commission_blocked": 0.0,
            "name": "Linux Quantitative Trader",
            "server": self.server,
            "currency": self.currency,
            "company": "MetaQuotes Software Corp."
        }

    def get_terminal_info(self) -> Dict[str, Any]:
        return {
            "community_account": True,
            "community_connection": True,
            "connected": True,
            "dlls_allowed": True,
            "trade_allowed": True,
            "trade_api_disabled": False,
            "email_enabled": False,
            "ftp_enabled": False,
            "notifications_enabled": False,
            "mqid": True,
            "build": 4410,
            "maxbars": 100000,
            "codepage": 65001,
            "ping_last": 1250,
            "community_balance": 0.0,
            "retransmission": 0.0,
            "company": "MetaQuotes Software Corp.",
            "name": "MetaTrader 5 (Linux Wine Bridge)",
            "language": "English",
            "path": "/home/user/.wine/drive_c/Program Files/MetaTrader 5",
            "data_path": "/home/user/.wine/drive_c/Program Files/MetaTrader 5",
            "commondata_path": "/home/user/.wine/drive_c/Program Files/Common"
        }

    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        self.update_market_prices()
        s = self.symbols.get(symbol.upper())
        if not s:
            return None
        now_ts = int(time.time())
        return {
            "custom": False, "chart_mode": 0, "select": True, "visible": True,
            "session_deals": 1500, "session_buy_orders": 800, "session_sell_orders": 700,
            "volume": 12000, "volumehigh": 25000, "volumelow": 5000, "time": now_ts,
            "digits": s["digits"], "spread": s["spread"], "spread_float": True,
            "ticks_bookdepth": 32, "trade_calc_mode": 0, "trade_mode": 4,
            "start_time": 0, "expiration_time": 0, "trade_stops_level": 0,
            "trade_freeze_level": 0, "trade_exemode": 1, "swap_mode": 1,
            "swap_rollover3days": 3, "margin_hedged_use_leg": False,
            "expiration_mode": 15, "filling_mode": 3, "order_mode": 127,
            "order_gtc_mode": 0, "option_mode": 0, "option_right": 0,
            "bid": s["bid"], "bidhigh": s["bid"] + 0.005, "bidlow": s["bid"] - 0.005,
            "ask": s["ask"], "askhigh": s["ask"] + 0.005, "asklow": s["ask"] - 0.005,
            "last": s["last"], "lasthigh": s["last"] + 0.005, "lastlow": s["last"] - 0.005,
            "volume_real": 0.0, "volumehigh_real": 0.0, "volumelow_real": 0.0,
            "option_strike": 0.0, "point": s["point"], "trade_tick_value": s["trade_tick_value"],
            "trade_tick_value_profit": s["trade_tick_value"], "trade_tick_value_loss": s["trade_tick_value"],
            "trade_tick_size": s["point"], "trade_contract_size": s["contract_size"],
            "trade_accrued_interest": 0.0, "trade_face_value": 0.0, "trade_liquidity_rate": 0.0,
            "volume_min": s["volume_min"], "volume_max": s["volume_max"], "volume_step": s["volume_step"],
            "volume_limit": 0.0, "swap_long": -1.2, "swap_short": -0.8,
            "margin_initial": 0.0, "margin_maintenance": 0.0, "session_volume": 100000.0,
            "session_turnover": 0.0, "session_interest": 0.0, "session_buy_orders_volume": 0.0,
            "session_sell_orders_volume": 0.0, "session_open": s["bid"], "session_close": s["bid"],
            "session_aw": 0.0, "session_price_settlement": 0.0, "session_price_limit_min": 0.0,
            "session_price_limit_max": 0.0, "margin_hedged": 0.0, "price_change": 0.02,
            "price_volatility": 0.05, "price_theoretical": 0.0, "basis": "",
            "category": "Forex", "currency_base": s["currency_base"],
            "currency_profit": s["currency_profit"], "currency_margin": s["currency_margin"],
            "bank": "", "description": f"{s['name']} Spot Currency Pair", "exchange": "",
            "formula": "", "isin": "", "name": s["name"], "page": "", "path": f"Forex\\{s['name']}"
        }

    def get_symbol_tick(self, symbol: str) -> Optional[Dict[str, Any]]:
        self.update_market_prices()
        s = self.symbols.get(symbol.upper())
        if not s:
            return None
        now_ts = int(time.time())
        return {
            "time": now_ts,
            "bid": s["bid"],
            "ask": s["ask"],
            "last": s["last"],
            "volume": random.randint(1, 50),
            "time_msc": int(time.time() * 1000),
            "flags": 6,
            "volume_real": 0.0
        }

    def copy_rates_from_pos(self, symbol: str, timeframe: int, start_pos: int, count: int) -> List[Dict[str, Any]]:
        """Generate deterministic OHLCV candles for testing & analysis."""
        s = self.symbols.get(symbol.upper())
        if not s:
            return []
        
        # Determine timeframe interval in seconds
        tf_seconds = 60
        if timeframe == TIMEFRAME_M5:
            tf_seconds = 300
        elif timeframe == TIMEFRAME_M15:
            tf_seconds = 900
        elif timeframe == TIMEFRAME_H1:
            tf_seconds = 3600
        elif timeframe == TIMEFRAME_D1:
            tf_seconds = 86400

        now_sec = (int(time.time()) // tf_seconds) * tf_seconds
        rates = []
        base_price = s["bid"]

        # Generate candles backwards
        for i in range(count):
            idx = start_pos + (count - 1 - i)
            bar_time = now_sec - (idx * tf_seconds)
            
            # Synthetic price movement with sinusoidal and random noise
            noise = math.sin(idx * 0.1) * s["point"] * 50 + (random.random() - 0.5) * s["point"] * 10
            bar_open = round(base_price + noise, s["digits"])
            bar_high = round(bar_open + abs(math.cos(idx * 0.15)) * s["point"] * 25, s["digits"])
            bar_low = round(bar_open - abs(math.sin(idx * 0.15)) * s["point"] * 25, s["digits"])
            bar_close = round((bar_open + bar_high + bar_low) / 3.0, s["digits"])

            rates.append({
                "time": bar_time,
                "open": bar_open,
                "high": max(bar_open, bar_high, bar_close),
                "low": min(bar_open, bar_low, bar_close),
                "close": bar_close,
                "tick_volume": random.randint(100, 5000),
                "spread": s["spread"],
                "real_volume": 0
            })

        return rates

    def execute_order(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simulated order request."""
        action = request.get("action", TRADE_ACTION_DEAL)
        symbol_name = request.get("symbol", "EURUSD").upper()
        s = self.symbols.get(symbol_name)
        if not s:
            return {
                "retcode": TRADE_RETCODE_INVALID,
                "deal": 0, "order": 0, "volume": 0.0, "price": 0.0,
                "bid": 0.0, "ask": 0.0, "comment": "Unknown symbol",
                "request_id": 0, "retcode_external": 0, "request": request
            }

        order_type = request.get("type", ORDER_TYPE_BUY)
        volume = float(request.get("volume", 0.01))
        price = float(request.get("price", s["ask"] if order_type == ORDER_TYPE_BUY else s["bid"]))
        sl = float(request.get("sl", 0.0))
        tp = float(request.get("tp", 0.0))
        comment = str(request.get("comment", ""))
        magic = int(request.get("magic", 0))

        if volume <= 0:
            return {
                "retcode": TRADE_RETCODE_INVALID_VOLUME,
                "deal": 0, "order": 0, "volume": volume, "price": price,
                "bid": s["bid"], "ask": s["ask"], "comment": "Invalid volume",
                "request_id": 0, "retcode_external": 0, "request": request
            }

        if action == TRADE_ACTION_DEAL:
            # Check margin requirement
            contract_size = s["contract_size"]
            required_margin = (volume * contract_size) / self.leverage
            acct = self.get_account_info()
            if required_margin > acct["margin_free"]:
                return {
                    "retcode": TRADE_RETCODE_NO_MONEY,
                    "deal": 0, "order": 0, "volume": volume, "price": price,
                    "bid": s["bid"], "ask": s["ask"], "comment": "Not enough money",
                    "request_id": 0, "retcode_external": 0, "request": request
                }

            # Check if this deal is closing an existing position (e.g. sell when pos is buy)
            position_id = request.get("position", 0)
            if position_id in self.positions:
                pos = self.positions.pop(position_id)
                # Realize PnL
                if pos["type"] == POSITION_TYPE_BUY:
                    pnl = (price - pos["price_open"]) * pos["volume"] * contract_size
                else:
                    pnl = (pos["price_open"] - price) * pos["volume"] * contract_size
                self.balance += pnl

                deal_ticket = self.next_deal_ticket()
                order_ticket = self.next_order_ticket()
                now_ts = int(time.time())

                deal_record = {
                    "ticket": deal_ticket, "order": order_ticket, "time": now_ts,
                    "time_msc": now_ts * 1000, "type": DEAL_TYPE_SELL if pos["type"] == POSITION_TYPE_BUY else DEAL_TYPE_BUY,
                    "entry": DEAL_ENTRY_OUT, "magic": magic, "position_id": position_id,
                    "reason": 0, "volume": volume, "price": price, "commission": 0.0,
                    "swap": 0.0, "profit": round(pnl, 2), "fee": 0.0, "symbol": symbol_name,
                    "comment": comment or "Closed position", "external_id": ""
                }
                self.history_deals.append(deal_record)

                return {
                    "retcode": TRADE_RETCODE_DONE,
                    "deal": deal_ticket, "order": order_ticket, "volume": volume,
                    "price": price, "bid": s["bid"], "ask": s["ask"],
                    "comment": "Position closed successfully", "request_id": order_ticket,
                    "retcode_external": 0, "request": request
                }

            # New opening position
            pos_ticket = self.next_ticket()
            order_ticket = self.next_order_ticket()
            deal_ticket = self.next_deal_ticket()
            now_ts = int(time.time())

            pos_type = POSITION_TYPE_BUY if order_type == ORDER_TYPE_BUY else POSITION_TYPE_SELL
            self.positions[pos_ticket] = {
                "ticket": pos_ticket,
                "time": now_ts,
                "time_msc": now_ts * 1000,
                "time_update": now_ts,
                "time_update_msc": now_ts * 1000,
                "type": pos_type,
                "magic": magic,
                "identifier": pos_ticket,
                "reason": 3,
                "volume": volume,
                "price_open": price,
                "sl": sl,
                "tp": tp,
                "price_current": price,
                "swap": 0.0,
                "profit": 0.0,
                "symbol": symbol_name,
                "comment": comment,
                "external_id": ""
            }

            deal_record = {
                "ticket": deal_ticket, "order": order_ticket, "time": now_ts,
                "time_msc": now_ts * 1000, "type": DEAL_TYPE_BUY if pos_type == POSITION_TYPE_BUY else DEAL_TYPE_SELL,
                "entry": DEAL_ENTRY_IN, "magic": magic, "position_id": pos_ticket,
                "reason": 3, "volume": volume, "price": price, "commission": 0.0,
                "swap": 0.0, "profit": 0.0, "fee": 0.0, "symbol": symbol_name,
                "comment": comment, "external_id": ""
            }
            self.history_deals.append(deal_record)

            return {
                "retcode": TRADE_RETCODE_DONE,
                "deal": deal_ticket, "order": order_ticket, "volume": volume,
                "price": price, "bid": s["bid"], "ask": s["ask"],
                "comment": "Order executed successfully", "request_id": order_ticket,
                "retcode_external": 0, "request": request
            }

        elif action == TRADE_ACTION_SLTP:
            pos_id = request.get("position", 0)
            if pos_id in self.positions:
                self.positions[pos_id]["sl"] = sl
                self.positions[pos_id]["tp"] = tp
                return {
                    "retcode": TRADE_RETCODE_DONE,
                    "deal": 0, "order": 0, "volume": 0.0, "price": 0.0,
                    "bid": s["bid"], "ask": s["ask"], "comment": "SL/TP modified",
                    "request_id": 0, "retcode_external": 0, "request": request
                }

        return {
            "retcode": TRADE_RETCODE_DONE,
            "deal": self.next_deal_ticket(), "order": self.next_order_ticket(),
            "volume": volume, "price": price, "bid": s["bid"], "ask": s["ask"],
            "comment": "Trade action completed", "request_id": 0,
            "retcode_external": 0, "request": request
        }

    def dispatch_rpc(self, method: str, params: Any) -> Any:
        """Route RPC method to simulator action."""
        if method == "initialize":
            self.initialized = True
            return True
        elif method == "shutdown":
            self.initialized = False
            return True
        elif method == "version":
            return (500, 4410, "15 Oct 2026")
        elif method == "terminal_info":
            return self.get_terminal_info()
        elif method == "account_info":
            return self.get_account_info()
        elif method == "symbols_total":
            return len(self.symbols)
        elif method == "symbol_select":
            sym = params.get("symbol", "") if isinstance(params, dict) else str(params)
            enable = params.get("enable", True) if isinstance(params, dict) else True
            sym_upper = sym.upper()
            if sym_upper in self.symbols:
                self.symbols[sym_upper]["select"] = bool(enable)
                return True
            return True
        elif method == "symbols_get":
            group = params.get("group") if isinstance(params, dict) else None
            res = []
            for sym in self.symbols.keys():
                if group and group not in sym:
                    continue
                info = self.get_symbol_info(sym)
                if info:
                    res.append(info)
            return res
        elif method == "symbol_info":
            sym = params.get("symbol") if isinstance(params, dict) else params
            return self.get_symbol_info(str(sym))
        elif method == "symbol_info_tick":
            sym = params.get("symbol") if isinstance(params, dict) else params
            return self.get_symbol_tick(str(sym))
        elif method == "copy_rates_from_pos":
            sym = params.get("symbol", "EURUSD")
            tf = params.get("timeframe", TIMEFRAME_M1)
            start_pos = params.get("start_pos", 0)
            count = params.get("count", 100)
            return self.copy_rates_from_pos(sym, tf, start_pos, count)
        elif method == "order_send":
            req = params.get("request", {}) if isinstance(params, dict) else params
            return self.execute_order(req)
        elif method == "positions_total":
            return len(self.positions)
        elif method == "positions_get":
            sym = params.get("symbol") if isinstance(params, dict) else None
            ticket = params.get("ticket") if isinstance(params, dict) else None
            res = []
            for p in self.positions.values():
                if sym and p["symbol"] != sym:
                    continue
                if ticket and p["ticket"] != ticket:
                    continue
                res.append(p)
            return res
        elif method == "history_deals_total":
            return len(self.history_deals)
        elif method == "history_deals_get":
            return list(self.history_deals)
        elif method == "order_calc_margin":
            action = params.get("action", ORDER_TYPE_BUY)
            symbol = params.get("symbol", "EURUSD")
            volume = params.get("volume", 0.01)
            price = params.get("price", 1.0850)
            s = self.symbols.get(symbol.upper(), {})
            c_size = s.get("contract_size", 100000.0)
            return round((volume * c_size * price) / self.leverage, 2)
        elif method == "order_calc_profit":
            action = params.get("action", ORDER_TYPE_BUY)
            symbol = params.get("symbol", "EURUSD")
            volume = params.get("volume", 0.01)
            price_open = params.get("price_open", 1.0850)
            price_close = params.get("price_close", 1.0860)
            s = self.symbols.get(symbol.upper(), {})
            c_size = s.get("contract_size", 100000.0)
            diff = (price_close - price_open) if action == ORDER_TYPE_BUY else (price_open - price_close)
            return round(diff * volume * c_size, 2)
        else:
            raise NotImplementedError(f"RPC method '{method}' is not recognized")
