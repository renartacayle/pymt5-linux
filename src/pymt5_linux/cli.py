"""Command-line interface (CLI) for pymt5-linux."""

import sys
import argparse
import logging
import time

from ._version import __version__
from .gateway import MT5GatewayServer
from .client import MetaTrader5Client
from .wine_manager import (
    is_wine_installed,
    get_wine_version,
    is_xvfb_installed,
    find_mt5_terminals
)


def setup_cli_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )


def cmd_status(args: argparse.Namespace) -> int:
    """Check Linux system readiness for MT5 and Wine."""
    print("=" * 65)
    print(f" pymt5-linux System Diagnostics (v{__version__})")
    print("=" * 65)

    # Wine
    wine_ok = is_wine_installed()
    wine_ver = get_wine_version() if wine_ok else "Not Installed"
    status_icon = "✓" if wine_ok else "✗"
    print(f"[{status_icon}] Wine Runtime    : {wine_ver}")

    # Xvfb
    xvfb_ok = is_xvfb_installed()
    xvfb_icon = "✓" if xvfb_ok else "✗"
    xvfb_text = "Installed (Ready for headless servers)" if xvfb_ok else "Not Installed (Install with: sudo apt install xvfb)"
    print(f"[{xvfb_icon}] Headless Display : {xvfb_text}")

    # MT5 Terminals
    terminals = find_mt5_terminals()
    term_icon = "✓" if terminals else "!"
    print(f"[{term_icon}] MT5 Terminals   : Found {len(terminals)} installed terminal(s)")
    for t in terminals:
        print(f"    -> {t}")

    # Gateway Check
    client = MetaTrader5Client()
    connected = client.initialize(host=args.host, port=args.port, auto_start_mock=False)
    if connected:
        acct = client.account_info()
        print(f"[✓] Gateway Server   : Running on {args.host}:{args.port}")
        if acct:
            print(f"    Account Login   : {acct.login} ({acct.server})")
            print(f"    Balance / Equity: {acct.balance} / {acct.equity} {acct.currency}")
        client.shutdown()
    else:
        print(f"[-] Gateway Server   : Not running on {args.host}:{args.port}")

    print("=" * 65)
    return 0


def cmd_mock(args: argparse.Namespace) -> int:
    """Run standalone in-memory mock simulator server."""
    setup_cli_logging(args.verbose)
    print(f"Starting MT5 Mock Simulator Server on {args.host}:{args.port}...")
    server = MT5GatewayServer(host=args.host, port=args.port, force_mock=True, balance=args.balance)
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        print("\nStopping Mock Simulator...")
        server.stop()
    return 0


def cmd_gateway(args: argparse.Namespace) -> int:
    """Run Wine gateway bridge server."""
    setup_cli_logging(args.verbose)
    print(f"Starting MT5 Bridge Gateway on {args.host}:{args.port}...")
    server = MT5GatewayServer(host=args.host, port=args.port, force_mock=args.mock, balance=args.balance)
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        print("\nStopping Gateway...")
        server.stop()
    return 0


def cmd_test_connect(args: argparse.Namespace) -> int:
    """Test connection and measure latency to MT5 Gateway."""
    print(f"Testing connection to MT5 Gateway at {args.host}:{args.port}...")
    client = MetaTrader5Client()
    t0 = time.perf_counter()
    ok = client.initialize(host=args.host, port=args.port, auto_start_mock=args.auto_mock)
    latency_ms = (time.perf_counter() - t0) * 1000

    if not ok:
        err = client.last_error()
        print(f"FAILED to connect: {err[1]} (Code: {err[0]})")
        return 1

    print(f"SUCCESS: Connected in {latency_ms:.2f} ms")
    acct = client.account_info()
    if acct:
        print(f"Login   : {acct.login}")
        print(f"Server  : {acct.server}")
        print(f"Balance : {acct.balance} {acct.currency}")
        print(f"Equity  : {acct.equity} {acct.currency}")

    # Benchmark tick fetch
    t_tick = time.perf_counter()
    tick = client.symbol_info_tick("EURUSD")
    tick_lat = (time.perf_counter() - t_tick) * 1000
    if tick:
        print(f"EURUSD  : Bid={tick.bid} Ask={tick.ask} (Query Latency: {tick_lat:.2f} ms)")

    client.shutdown()
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pymt5-linux",
        description="Production-grade MetaTrader 5 SDK and Drop-in Replacement for Linux"
    )
    parser.add_argument("-v", "--version", action="version", version=f"pymt5-linux {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Status
    p_status = subparsers.add_parser("status", help="Check system readiness, Wine, and MT5")
    p_status.add_argument("--host", default="127.0.0.1", help="Gateway host")
    p_status.add_argument("--port", type=int, default=18812, help="Gateway port")

    # Mock Server
    p_mock = subparsers.add_parser("mock", help="Start standalone mock simulator server")
    p_mock.add_argument("--host", default="127.0.0.1", help="Bind host")
    p_mock.add_argument("--port", type=int, default=18812, help="Bind port")
    p_mock.add_argument("--balance", type=float, default=10000.0, help="Initial mock balance")
    p_mock.add_argument("--verbose", action="store_true", help="Enable verbose debug logs")

    # Gateway Server
    p_gw = subparsers.add_parser("gateway", help="Start bridge gateway server (in Wine or host)")
    p_gw.add_argument("--host", default="127.0.0.1", help="Bind host")
    p_gw.add_argument("--port", type=int, default=18812, help="Bind port")
    p_gw.add_argument("--mock", action="store_true", help="Force mock engine mode")
    p_gw.add_argument("--balance", type=float, default=10000.0, help="Initial balance if mock")
    p_gw.add_argument("--verbose", action="store_true", help="Enable verbose debug logs")

    # Test Connect
    p_test = subparsers.add_parser("test-connect", help="Test connection and measure latency")
    p_test.add_argument("--host", default="127.0.0.1", help="Gateway host")
    p_test.add_argument("--port", type=int, default=18812, help="Gateway port")
    p_test.add_argument("--auto-mock", action="store_true", help="Auto start mock server if unavailable")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "status":
        sys.exit(cmd_status(args))
    elif args.command == "mock":
        sys.exit(cmd_mock(args))
    elif args.command == "gateway":
        sys.exit(cmd_gateway(args))
    elif args.command == "test-connect":
        sys.exit(cmd_test_connect(args))


if __name__ == "__main__":
    main()
