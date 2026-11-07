"""Error codes and exceptions matching official MetaTrader 5 Python API."""

from typing import Tuple

# Standard MT5 Return Codes (RES_*)
RES_S_OK = 1
RES_E_FAIL = -1
RES_E_INVALID_PARAMS = -2
RES_E_NO_MEMORY = -3
RES_E_NOT_FOUND = -4
RES_E_INVALID_VERSION = -5
RES_E_AUTH_FAILED = -6
RES_E_UNSUPPORTED = -7
RES_E_AUTO_TRADING_DISABLED = -8
RES_E_INTERNAL_FAIL = -10000
RES_E_INTERNAL_FAIL_SEND = -10001
RES_E_INTERNAL_FAIL_RECEIVE = -10002
RES_E_INTERNAL_FAIL_INIT = -10003
RES_E_INTERNAL_FAIL_CONNECT = -10004
RES_E_INTERNAL_FAIL_TIMEOUT = -10005

ERROR_DESCRIPTIONS = {
    RES_S_OK: "Success",
    RES_E_FAIL: "Generic failure",
    RES_E_INVALID_PARAMS: "Invalid parameters",
    RES_E_NO_MEMORY: "Not enough memory",
    RES_E_NOT_FOUND: "Requested item not found",
    RES_E_INVALID_VERSION: "Invalid version",
    RES_E_AUTH_FAILED: "Authorization failed",
    RES_E_UNSUPPORTED: "Unsupported method or operation",
    RES_E_AUTO_TRADING_DISABLED: "Auto trading disabled in terminal",
    RES_E_INTERNAL_FAIL: "Internal IPC failure",
    RES_E_INTERNAL_FAIL_SEND: "IPC send failure",
    RES_E_INTERNAL_FAIL_RECEIVE: "IPC receive failure",
    RES_E_INTERNAL_FAIL_INIT: "IPC initialization failure",
    RES_E_INTERNAL_FAIL_CONNECT: "Failed to connect to MT5 bridge or terminal",
    RES_E_INTERNAL_FAIL_TIMEOUT: "IPC operation timed out",
}


def format_error(code: int, custom_msg: str = "") -> Tuple[int, str]:
    """Format error code and description into standard MT5 tuple format (code, description)."""
    desc = custom_msg or ERROR_DESCRIPTIONS.get(code, f"Unknown error code {code}")
    return (code, desc)


class MT5Error(Exception):
    """Base exception for MetaTrader 5 errors."""

    def __init__(self, code: int, message: str = "") -> None:
        self.code = code
        self.message = message or ERROR_DESCRIPTIONS.get(code, f"Error {code}")
        super().__init__(f"[{self.code}] {self.message}")


class MT5ConnectionError(MT5Error):
    """Raised when communication with MT5 or the Wine Gateway fails."""

    def __init__(self, message: str = "Connection to MT5 Gateway failed") -> None:
        super().__init__(RES_E_INTERNAL_FAIL_CONNECT, message)


class MT5TimeoutError(MT5Error):
    """Raised when an operation times out."""

    def __init__(self, message: str = "MT5 operation timed out") -> None:
        super().__init__(RES_E_INTERNAL_FAIL_TIMEOUT, message)
