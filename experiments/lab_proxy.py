#!/usr/bin/env python3
"""
Lab CONNECT proxy with two variants:
  - Variant A (normal, port 8888): standard CONNECT behavior
  - Variant B (speculative, port 8889): sends 200 before connecting to target

Usage: python3 lab_proxy.py
"""

import socket
import select
import threading
import sys
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/tmp/lab_proxy.log"),
    ],
)
log = logging.getLogger("labproxy")

NORMAL_PORT = 8888
SPECULATIVE_PORT = 8889
BUFFER_SIZE = 65536
TARGET_TIMEOUT = 5


def forward(sock_a, sock_b):
    """Bidirectional byte forwarding until one side closes."""
    sockets = [sock_a, sock_b]
    try:
        while True:
            readable, _, errored = select.select(sockets, [], sockets, 30)
            if errored:
                break
            for s in readable:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    return
                other = sock_b if s is sock_a else sock_a
                other.sendall(data)
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        sock_a.close()
        sock_b.close()


def parse_connect(data):
    """Parse CONNECT request, return (host, port) or None."""
    try:
        line = data.split(b"\r\n")[0].decode()
        parts = line.split()
        if len(parts) < 2 or parts[0] != "CONNECT":
            return None
        host_port = parts[1]
        if ":" in host_port:
            host, port = host_port.rsplit(":", 1)
            return host, int(port)
        return host_port, 443
    except Exception:
        return None


def handle_normal(client_sock, addr):
    """Variant A: Standard CONNECT proxy."""
    try:
        data = client_sock.recv(BUFFER_SIZE)
        if not data:
            client_sock.close()
            return

        target = parse_connect(data)
        if not target:
            client_sock.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_sock.close()
            return

        host, port = target
        log.info(f"[NORMAL] {addr[0]}:{addr[1]} -> {host}:{port}")

        # Connect to target first
        target_sock = socket.create_connection((host, port), timeout=TARGET_TIMEOUT)

        # Then send 200 to client
        client_sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

        # Bidirectional forwarding
        forward(client_sock, target_sock)

    except Exception as e:
        log.error(f"[NORMAL] {addr}: {e}")
        client_sock.close()


def handle_speculative(client_sock, addr):
    """Variant B: Speculative buffering — send 200 before connecting."""
    failures = {"count": 0}
    try:
        data = client_sock.recv(BUFFER_SIZE)
        if not data:
            client_sock.close()
            return

        target = parse_connect(data)
        if not target:
            client_sock.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_sock.close()
            return

        host, port = target
        log.info(f"[SPECULATIVE] {addr[0]}:{addr[1]} -> {host}:{port}")

        # Send 200 IMMEDIATELY (before connecting to target!)
        client_sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

        # Read client's first data (should be ClientHello)
        client_sock.settimeout(10)
        buffered = client_sock.recv(BUFFER_SIZE)
        if not buffered:
            client_sock.close()
            return

        # NOW connect to target
        try:
            target_sock = socket.create_connection((host, port), timeout=TARGET_TIMEOUT)
        except Exception as e:
            log.error(f"[SPECULATIVE] Target connection failed after 200 sent: {e}")
            client_sock.close()
            return

        # Send buffered ClientHello immediately after TCP handshake completes
        target_sock.sendall(buffered)

        # Continue bidirectional forwarding
        client_sock.settimeout(None)
        forward(client_sock, target_sock)

    except Exception as e:
        log.error(f"[SPECULATIVE] {addr}: {e}")
        client_sock.close()


def run_server(port, handler, name):
    """Run a proxy server on the given port."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(128)
    log.info(f"[{name}] Listening on port {port}")

    while True:
        client_sock, addr = server.accept()
        t = threading.Thread(target=handler, args=(client_sock, addr), daemon=True)
        t.start()


def main():
    log.info("Starting lab proxy...")
    log.info(f"  Normal proxy:      port {NORMAL_PORT}")
    log.info(f"  Speculative proxy: port {SPECULATIVE_PORT}")

    t1 = threading.Thread(target=run_server, args=(NORMAL_PORT, handle_normal, "NORMAL"), daemon=True)
    t2 = threading.Thread(target=run_server, args=(SPECULATIVE_PORT, handle_speculative, "SPECULATIVE"), daemon=True)

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Shutting down")


if __name__ == "__main__":
    main()
