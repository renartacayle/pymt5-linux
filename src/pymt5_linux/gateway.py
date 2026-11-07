"""Gateway bridge daemon running inside Wine or as standalone simulation server.

Listens for incoming client connections from Linux host and dispatches
requests to official MetaTrader 5 C-API (if available) or the Mock Engine.
"""

import sys
import socket
import select
import logging
import threading
from typing import Dict, Any, Optional

from .protocol import receive_packet, send_packet
from .mock_engine import MockMT5Engine
from .errors import RES_S_OK, RES_E_FAIL

logger = logging.getLogger("pymt5_linux.gateway")

# Attempt importing official MetaTrader5 if running inside Wine / Windows
_REAL_MT5 = None
try:
    import MetaTrader5 as _mt5_module
    _REAL_MT5 = _mt5_module
except ImportError:
    _REAL_MT5 = None


class MT5GatewayServer:
    """Multi-threaded TCP server bridging Linux clients to MT5."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 18812,
        force_mock: bool = False,
        balance: float = 10000.0,
    ) -> None:
        self.host = host
        self.port = port
        self.force_mock = force_mock
        self.running = False
        self.server_sock: Optional[socket.socket] = None
        self.clients: list = []
        self._lock = threading.Lock()

        if _REAL_MT5 is not None and not force_mock:
            self.use_real_mt5 = True
            logger.info("Official MetaTrader5 library detected. Running in NATIVE BRIDGE mode.")
        else:
            self.use_real_mt5 = False
            self.mock_engine = MockMT5Engine(balance=balance)
            logger.info("Running in HIGH-FIDELITY SIMULATION / MOCK mode.")

    def handle_client(self, client_sock: socket.socket, addr: tuple) -> None:
        """Handle individual client request loop."""
        logger.info(f"Accepted connection from {addr}")
        try:
            while self.running:
                try:
                    req = receive_packet(client_sock)
                except (ConnectionResetError, EOFError):
                    break
                except Exception as e:
                    logger.debug(f"Client disconnected or read error: {e}")
                    break

                req_id = req.get("id", "")
                method = req.get("method", "")
                params = req.get("params", {})

                resp_data: Dict[str, Any] = {"id": req_id, "result": None, "error": None}

                try:
                    if self.use_real_mt5:
                        result = self._dispatch_real_mt5(method, params)
                    else:
                        result = self.mock_engine.dispatch_rpc(method, params)
                    resp_data["result"] = result
                except Exception as err:
                    logger.error(f"Error handling RPC '{method}': {err}")
                    resp_data["error"] = {"code": RES_E_FAIL, "message": str(err)}

                try:
                    send_packet(client_sock, resp_data)
                except Exception as e:
                    logger.error(f"Failed sending response to {addr}: {e}")
                    break
        finally:
            with self._lock:
                if client_sock in self.clients:
                    self.clients.remove(client_sock)
            client_sock.close()
            logger.info(f"Connection from {addr} closed")

    def _dispatch_real_mt5(self, method: str, params: Any) -> Any:
        """Execute call against official MetaTrader5 C-extension."""
        if not hasattr(_REAL_MT5, method):
            raise NotImplementedError(f"Method {method} not available in MetaTrader5")
        func = getattr(_REAL_MT5, method)

        if isinstance(params, dict):
            return func(**params)
        elif isinstance(params, (list, tuple)):
            return func(*params)
        elif params is None:
            return func()
        else:
            return func(params)

    def start(self, blocking: bool = True) -> None:
        """Start listening on the specified port."""
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(128)
        self.running = True

        logger.info(f"MT5 Gateway listening on {self.host}:{self.port}")

        if blocking:
            self._serve()
        else:
            t = threading.Thread(target=self._serve, daemon=True)
            t.start()

    def _serve(self) -> None:
        """Internal accept loop."""
        while self.running and self.server_sock:
            try:
                self.server_sock.settimeout(1.0)
                try:
                    client_sock, addr = self.server_sock.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break

                with self._lock:
                    self.clients.append(client_sock)

                t = threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True)
                t.start()
            except Exception as e:
                if self.running:
                    logger.error(f"Accept loop error: {e}")

    def stop(self) -> None:
        """Stop server and clean up client sockets."""
        self.running = False
        if self.server_sock:
            try:
                self.server_sock.close()
            except Exception:
                pass
            self.server_sock = None

        with self._lock:
            for s in self.clients:
                try:
                    s.close()
                except Exception:
                    pass
            self.clients.clear()
        logger.info("MT5 Gateway stopped")
