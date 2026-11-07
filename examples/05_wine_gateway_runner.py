#!/usr/bin/env python3
"""Example 05: Wine Gateway Bridge Runner.

Run this inside your Wine prefix where official MetaTrader 5 is installed:
    wine python examples/05_wine_gateway_runner.py --port 18812
"""

import argparse
from pymt5_linux.gateway import MT5GatewayServer

def main():
    parser = argparse.ArgumentParser(description="Run MT5 Wine Bridge Gateway Daemon")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=18812, help="Port to listen on")
    parser.add_argument("--mock", action="store_true", help="Force mock simulation mode")
    args = parser.parse_args()

    print(f"Starting MT5 Bridge Gateway on {args.host}:{args.port} (Mock={args.mock})...")
    server = MT5GatewayServer(host=args.host, port=args.port, force_mock=args.mock)
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        print("\nStopping gateway daemon...")
        server.stop()

if __name__ == "__main__":
    main()
