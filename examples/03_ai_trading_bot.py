#!/usr/bin/env python3
"""Example 03: Full AI Trading Agent running natively on Linux with MT5 Wine Bridge."""

import time
import numpy as np
import pymt5_linux as mt5

class AITradingAgent:
    def __init__(self, symbol: str = "EURUSD", magic_number: int = 777001):
        self.symbol = symbol
        self.magic = magic_number

    def extract_features(self, df):
        """Feature engineering pipeline for ML/AI models."""
        close = df["close"].values
        returns = np.diff(close) / close[:-1]
        volatility = np.std(returns[-20:]) if len(returns) >= 20 else 0.001
        momentum = (close[-1] - close[-10]) / close[-10] if len(close) >= 10 else 0.0
        return {"momentum": momentum, "volatility": volatility, "last_price": close[-1]}

    def predict_signal(self, features) -> int:
        """Simulate neural network or gradient boosted model inference.
        Returns: 1 for BUY, -1 for SELL, 0 for HOLD.
        """
        # Threshold logic representing model classification output
        if features["momentum"] > 0.0005:
            return 1
        elif features["momentum"] < -0.0005:
            return -1
        return 0

    def run_cycle(self):
        # 1. Fetch live market candles
        df = mt5.copy_rates_from_pos_df(self.symbol, mt5.TIMEFRAME_M1, 0, 60)
        if df.empty:
            print("Failed to retrieve market candles")
            return

        # 2. Extract features & infer AI signal
        features = self.extract_features(df)
        signal = self.predict_signal(features)
        print(f"[{self.symbol}] Price: {features['last_price']:.5f} | Momentum: {features['momentum']:.6f} | AI Signal: {signal}")

        # 3. Check existing positions
        positions = mt5.positions_get(symbol=self.symbol)
        my_positions = [p for p in (positions or []) if p.magic == self.magic]

        # 4. Execute orders based on signal
        tick = mt5.symbol_info_tick(self.symbol)
        if not tick:
            return

        if signal == 1 and len(my_positions) == 0:
            print("AI Signal: BUY triggered! Sending order...")
            req = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": 0.05,
                "type": mt5.ORDER_TYPE_BUY,
                "price": tick.ask,
                "sl": round(tick.ask - 0.0030, 5),
                "tp": round(tick.ask + 0.0060, 5),
                "magic": self.magic,
                "comment": "AI-Agent-V1-BUY"
            }
            res = mt5.order_send(req)
            print(f"Order result: {res.comment} (Ticket #{res.order})")

        elif signal == -1 and len(my_positions) > 0:
            print("AI Signal: Exit signal. Closing existing positions...")
            for pos in my_positions:
                close_req = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "position": pos.ticket,
                    "symbol": self.symbol,
                    "volume": pos.volume,
                    "type": mt5.ORDER_TYPE_SELL,
                    "price": tick.bid,
                    "magic": self.magic,
                    "comment": "AI-Agent-Close"
                }
                res = mt5.order_send(close_req)
                print(f"Closed #{pos.ticket}: {res.comment}")


def main():
    if not mt5.initialize():
        print(f"Connection failed: {mt5.last_error()}")
        return

    agent = AITradingAgent("EURUSD")
    print("AI Trading Agent initialized. Running trading loop (3 iterations)...")
    for step in range(3):
        agent.run_cycle()
        time.sleep(1)

    mt5.shutdown()
    print("AI Trading Agent stopped.")

if __name__ == "__main__":
    main()
