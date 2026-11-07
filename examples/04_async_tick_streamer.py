#!/usr/bin/env python3
"""Example 04: Real-time Event Streaming and Subscriptions."""

import time
import pymt5_linux as mt5
from pymt5_linux import MT5Streamer

def main():
    if not mt5.initialize():
        print(f"Init failed: {mt5.last_error()}")
        return

    streamer = MT5Streamer(mt5.default_client, poll_interval=0.1)

    @streamer.on_tick("EURUSD")
    def handle_eurusd(tick):
        print(f"[EURUSD Tick] Time: {tick.time} | Bid: {tick.bid:.5f} | Ask: {tick.ask:.5f}")

    @streamer.on_tick("BTCUSD")
    def handle_btcusd(tick):
        print(f"[BTCUSD Tick] Time: {tick.time} | Bid: ${tick.bid:,.2f} | Ask: ${tick.ask:,.2f}")

    print("Subscribed to EURUSD and BTCUSD ticks. Streaming for 5 seconds...")
    streamer.start()

    time.sleep(5)
    streamer.stop()
    mt5.shutdown()
    print("Streaming completed.")

if __name__ == "__main__":
    main()
