# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-07

### Added
- Complete 1:1 drop-in replacement API for official `MetaTrader5` on Linux.
- Ultra-low latency IPC / TCP gateway bridge (`MT5GatewayServer`) for Wine and remote VPS.
- `AsyncMetaTrader5` asynchronous client with non-blocking I/O.
- Real-time event streaming engine (`MT5Streamer`) with `@streamer.on_tick()` decorators.
- First-class Pandas DataFrame helpers: `copy_rates_from_pos_df()` with UTC datetime indexing.
- Complete high-fidelity mock simulator engine (`MockMT5Engine`) for local testing, CI/CD, and strategy backtesting.
- Full binary framing protocol with length-prefixed headers and payload validation.
- Command-line diagnostic and server manager (`pymt5-linux` / `mt5linux`).
- Wine process and headless display manager (`wine_manager.py`).
- Automated GitHub Actions CI workflow supporting Python 3.8 through 3.13.
- Production Dockerfile and docker-compose configurations.
