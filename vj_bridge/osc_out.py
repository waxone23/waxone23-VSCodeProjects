"""OSC output to Resolume. Sends only when a value has meaningfully changed."""

from __future__ import annotations

import threading

from pythonosc.udp_client import SimpleUDPClient


class OscSender:
    def __init__(self, ip: str, port: int) -> None:
        self._lock = threading.Lock()
        self._ip = ip
        self._port = port
        self._client = SimpleUDPClient(ip, port)
        self._last: dict[str, float] = {}

    def set_target(self, ip: str, port: int) -> None:
        with self._lock:
            if (ip, port) == (self._ip, self._port):
                return
            try:
                self._client = SimpleUDPClient(ip, port)
            except OSError:
                return  # bad address typed mid-edit; keep the old target
            self._ip, self._port = ip, port
            self._last.clear()

    def send(self, address: str, value: float) -> None:
        with self._lock:
            self._client.send_message(address, float(value))
            self._last[address] = float(value)

    def send_if_changed(self, address: str, value: float, epsilon: float = 0.005) -> None:
        with self._lock:
            if abs(value - self._last.get(address, -1e9)) <= epsilon:
                return
            self._client.send_message(address, float(value))
            self._last[address] = float(value)

    def snapshot(self) -> dict[str, float]:
        with self._lock:
            return dict(self._last)
