"""Tests for package exports, version, and pyproject metadata."""

import os
import pymt5_linux


def test_package_metadata():
    """Verify package metadata, version format, and core export bindings."""
    assert hasattr(pymt5_linux, "__version__")
    assert pymt5_linux.__version__ == "0.1.0"
    assert pymt5_linux.__author__ == "renartacayle"

    # Core classes
    assert hasattr(pymt5_linux, "MetaTrader5Client")
    assert hasattr(pymt5_linux, "AsyncMetaTrader5")
    assert hasattr(pymt5_linux, "MT5Streamer")
    assert hasattr(pymt5_linux, "MT5GatewayServer")
    assert hasattr(pymt5_linux, "MockMT5Engine")

    # Drop-in functions
    assert callable(pymt5_linux.initialize)
    assert callable(pymt5_linux.shutdown)
    assert callable(pymt5_linux.account_info)
    assert callable(pymt5_linux.order_send)
    assert callable(pymt5_linux.copy_rates_from_pos_df)


def test_pyproject_toml_exists():
    """Verify that pyproject.toml exists and contains required build information."""
    repo_root = os.path.dirname(os.path.dirname(__file__))
    pyproject_path = os.path.join(repo_root, "pyproject.toml")
    assert os.path.exists(pyproject_path)

    with open(pyproject_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "pymt5-linux" in content
    assert "build-backend = \"hatchling.build\"" in content
    assert "renartacayle" in content
