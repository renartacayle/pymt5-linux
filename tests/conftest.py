"""Pytest fixtures for pymt5-linux."""

import pytest
import time
import socket
from pymt5_linux.gateway import MT5GatewayServer
from pymt5_linux.client import MetaTrader5Client


@pytest.fixture(scope="function")
def free_port():
    """Find a guaranteed free port on localhost."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="function")
def running_mock_gateway(free_port):
    """Start a real TCP mock gateway on a free port for integration testing."""
    server = MT5GatewayServer(host="127.0.0.1", port=free_port, force_mock=True, balance=25000.0)
    server.start(blocking=False)
    time.sleep(0.05)  # Allow thread to bind socket
    yield ("127.0.0.1", free_port)
    server.stop()


@pytest.fixture
def mt5_client(running_mock_gateway):
    """Provide a connected MetaTrader5Client instance."""
    host, port = running_mock_gateway
    client = MetaTrader5Client()
    connected = client.initialize(host=host, port=port, auto_start_mock=False)
    assert connected is True, "Failed to connect client to mock gateway"
    yield client
    client.shutdown()
