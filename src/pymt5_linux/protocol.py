"""High-performance framing and serialization protocol for MT5 IPC / TCP bridge."""

import json
import struct
import socket
import asyncio
from typing import Dict, Any, Optional, Tuple, Union

# 4-byte unsigned integer big-endian header for message framing
HEADER_FORMAT = "!I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
MAX_PAYLOAD_SIZE = 64 * 1024 * 1024  # 64 MB maximum payload protection


def encode_packet(data: Dict[str, Any]) -> bytes:
    """Encode a Python dictionary to a length-prefixed JSON byte stream."""
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    payload_len = len(payload)
    if payload_len > MAX_PAYLOAD_SIZE:
        raise ValueError(f"Payload size {payload_len} exceeds maximum allowed {MAX_PAYLOAD_SIZE} bytes")
    header = struct.pack(HEADER_FORMAT, payload_len)
    return header + payload


def decode_header(header_bytes: bytes) -> int:
    """Unpack message length from 4-byte header."""
    if len(header_bytes) != HEADER_SIZE:
        raise ValueError(f"Header must be {HEADER_SIZE} bytes, got {len(header_bytes)}")
    length: int = struct.unpack(HEADER_FORMAT, header_bytes)[0]
    return length


def send_packet(sock: socket.socket, data: Dict[str, Any]) -> None:
    """Send length-prefixed packet over a blocking or non-blocking socket."""
    packet = encode_packet(data)
    sock.sendall(packet)


def receive_packet(sock: socket.socket, timeout: Optional[float] = None) -> Dict[str, Any]:
    """Receive and decode a length-prefixed packet from a socket."""
    if timeout is not None:
        sock.settimeout(timeout)
        
    # Read the 4-byte header
    header_buf = bytearray()
    while len(header_buf) < HEADER_SIZE:
        chunk = sock.recv(HEADER_SIZE - len(header_buf))
        if not chunk:
            raise ConnectionResetError("Connection closed while waiting for message header")
        header_buf.extend(chunk)

    payload_len = decode_header(bytes(header_buf))
    if payload_len > MAX_PAYLOAD_SIZE:
        raise ValueError(f"Incoming payload length {payload_len} exceeds maximum limit")

    # Read the payload
    payload_buf = bytearray()
    while len(payload_buf) < payload_len:
        needed = payload_len - len(payload_buf)
        chunk = sock.recv(min(needed, 65536))
        if not chunk:
            raise ConnectionResetError("Connection closed while receiving message payload")
        payload_buf.extend(chunk)

    return json.loads(payload_buf.decode("utf-8"))


async def async_send_packet(writer: asyncio.StreamWriter, data: Dict[str, Any]) -> None:
    """Send length-prefixed packet asynchronously via asyncio StreamWriter."""
    packet = encode_packet(data)
    writer.write(packet)
    await writer.drain()


async def async_receive_packet(reader: asyncio.StreamReader) -> Dict[str, Any]:
    """Receive and decode length-prefixed packet asynchronously via asyncio StreamReader."""
    header_bytes = await reader.readexactly(HEADER_SIZE)
    payload_len = decode_header(header_bytes)
    if payload_len > MAX_PAYLOAD_SIZE:
        raise ValueError(f"Incoming payload length {payload_len} exceeds maximum limit")
    payload_bytes = await reader.readexactly(payload_len)
    return json.loads(payload_bytes.decode("utf-8"))
