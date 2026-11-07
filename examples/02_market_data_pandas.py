#!/usr/bin/env python3
"""Example 02: Fetching Historical Candles to Pandas DataFrame and calculating SMA."""

import pymt5_linux as mt5

def main():
    if not mt5.initialize():
        print(f"Init error: {mt5.last_error()}")
        return

    symbol = "EURUSD"
    print(f"Fetching 100 M5 candles for {symbol}...")

    # Fetch directly as a Pandas DataFrame
    df = mt5.copy_rates_from_pos_df(symbol, mt5.TIMEFRAME_M5, start_pos=0, count=100)
    print("\nDataframe Overview:")
    print(df.info())

    # Calculate Simple Moving Averages (SMA)
    df["SMA_20"] = df["close"].rolling(window=20).mean()
    df["SMA_50"] = df["close"].rolling(window=50).mean()

    print("\nRecent Candles with Indicators:")
    print(df[["open", "high", "low", "close", "tick_volume", "SMA_20", "SMA_50"]].tail(10))

    mt5.shutdown()

if __name__ == "__main__":
    main()
