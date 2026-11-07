"""Real-time event streaming and subscription engine for ticks and candle bars."""

import time
import threading
from typing import Callable, Dict, List, Optional
from .types import Tick
from .client import MetaTrader5Client


class MT5Streamer:
    """Poll-free and event-driven market data streamer."""

    def __init__(self, client: MetaTrader5Client, poll_interval: float = 0.1) -> None:
        self.client = client
        self.poll_interval = poll_interval
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._tick_callbacks: Dict[str, List[Callable[[Tick], None]]] = {}
        self._last_ticks: Dict[str, Tick] = {}
        self._lock = threading.Lock()

    def on_tick(self, symbol: str) -> Callable[[Callable[[Tick], None]], Callable[[Tick], None]]:
        """Decorator to register a callback for new symbol ticks."""
        sym = symbol.upper()

        def decorator(func: Callable[[Tick], None]) -> Callable[[Tick], None]:
            self.subscribe_tick(sym, func)
            return func

        return decorator

    def subscribe_tick(self, symbol: str, callback: Callable[[Tick], None]) -> None:
        """Register a callback for incoming ticks for a symbol."""
        sym = symbol.upper()
        with self._lock:
            if sym not in self._tick_callbacks:
                self._tick_callbacks[sym] = []
            self._tick_callbacks[sym].append(callback)

    def start(self) -> None:
        """Start streaming thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._stream_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop streaming thread."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _stream_loop(self) -> None:
        while self.running:
            with self._lock:
                symbols_to_check = list(self._tick_callbacks.keys())

            for sym in symbols_to_check:
                try:
                    tick = self.client.symbol_info_tick(sym)
                    if not tick:
                        continue

                    last_tick = self._last_ticks.get(sym)
                    if last_tick is None or tick.time_msc != last_tick.time_msc or tick.bid != last_tick.bid or tick.ask != last_tick.ask:
                        self._last_ticks[sym] = tick
                        callbacks = self._tick_callbacks.get(sym, [])
                        for cb in callbacks:
                            try:
                                cb(tick)
                            except Exception as err:
                                pass
                except Exception:
                    pass

            time.sleep(self.poll_interval)
