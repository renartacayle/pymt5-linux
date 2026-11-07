#!/usr/bin/env python3
"""Example 01: Basic Connection and Account Inspection using drop-in API."""

import pymt5_linux as mt5

def main():
    print("Connecting to MetaTrader 5 (or local embedded simulator)...")
    if not mt5.initialize():
        print(f"Initialization failed: {mt5.last_error()}")
        return

    # Check terminal version and build
    v = mt5.version()
    print(f"MT5 Terminal Version: {v[0]}, Build: {v[1]}, Release: {v[2]}")

    # Inspect trading account
    acct = mt5.account_info()
    if acct:
        print("\n--- Account Overview ---")
        print(f"Login      : {acct.login}")
        print(f"Trader Name: {acct.name}")
        print(f"Server     : {acct.server}")
        print(f"Currency   : {acct.currency}")
        print(f"Leverage   : 1:{acct.leverage}")
        print(f"Balance    : ${acct.balance:,.2f}")
        print(f"Equity     : ${acct.equity:,.2f}")
        print(f"Margin Free: ${acct.margin_free:,.2f}")

    # Inspect financial instruments
    total = mt5.symbols_total()
    print(f"\nTotal Symbols Available: {total}")
    symbols = mt5.symbols_get()
    if symbols:
        print("Sample Symbols:")
        for s in symbols[:5]:
            print(f" - {s.name:8s} | Spread: {s.spread} pts | Digits: {s.digits}")

    mt5.shutdown()
    print("\nDisconnected successfully.")

if __name__ == "__main__":
    main()
