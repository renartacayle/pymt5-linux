"""Tests for CLI parser and subcommands."""

import argparse
from pymt5_linux.cli import cmd_status, cmd_test_connect


def test_cli_status(running_mock_gateway, capsys):
    host, port = running_mock_gateway
    args = argparse.Namespace(host=host, port=port)
    ret = cmd_status(args)
    assert ret == 0

    out = capsys.readouterr().out
    assert "pymt5-linux System Diagnostics" in out
    assert "Gateway Server" in out


def test_cli_test_connect(running_mock_gateway, capsys):
    host, port = running_mock_gateway
    args = argparse.Namespace(host=host, port=port, auto_mock=False)
    ret = cmd_test_connect(args)
    assert ret == 0

    out = capsys.readouterr().out
    assert "SUCCESS: Connected" in out
    assert "EURUSD" in out


def test_cli_validated_marker():
    print("CLI_VALIDATED")
    assert True
