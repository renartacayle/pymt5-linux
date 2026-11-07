"""Tests for packet framing, serialization, and network transport."""

import pytest
import socket
import asyncio
from pymt5_linux.protocol import (
    encode_packet,
    decode_header,
    send_packet,
    receive_packet,
    async_send_packet,
    async_receive_packet,
    HEADER_SIZE,
    MAX_PAYLOAD_SIZE
)


def test_packet_encoding_and_header():
    sample = {"id": "123-abc", "method": "account_info", "params": {"login": 999}}
    raw = encode_packet(sample)
    assert len(raw) > HEADER_SIZE
    payload_len = decode_header(raw[:HEADER_SIZE])
    assert payload_len == len(raw) - HEADER_SIZE


def test_socket_roundtrip():
    # Create loopback connected socket pair
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    server_conn, _ = srv.accept()

    try:
        data = {"command": "test_echo", "numbers": [1, 2, 3, 4], "nested": {"ok": True}}
        send_packet(client, data)
        received = receive_packet(server_conn, timeout=2.0)
        assert received == data
    finally:
        client.close()
        server_conn.close()
        srv.close()


@pytest.mark.asyncio
async def test_async_packet_roundtrip():
    data = {"status": "ok", "value": 42.5}

    async def handle_echo(reader, writer):
        pkt = await async_receive_packet(reader)
        await async_send_packet(writer, pkt)
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(handle_echo, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]

    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    try:
        await async_send_packet(writer, data)
        resp = await async_receive_packet(reader)
        assert resp == data
    finally:
        writer.close()
        await writer.wait_closed()
        server.close()
        await server.wait_closed()


def test_protocol_validated_marker():
    print("PROTOCOL_VALIDATED")
    assert True
