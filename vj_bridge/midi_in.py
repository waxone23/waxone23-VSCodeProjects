"""MIDI controller input (APC40 MKII, or any controller that sends CC messages).

MidiRouter is plain Python (thread-safe, no MIDI library) so it is easy to test.
MidiInput is the thin mido/rtmidi wrapper that feeds it.
"""

from __future__ import annotations

import threading

from .config import MidiBinding

MIDI_NONE = "__none__"  # combo-box value meaning "no controller"


def pick_default_port(ports: list[str]) -> str | None:
    """Auto-detect an APC40 among the available MIDI input ports."""
    for port in ports:
        if "apc40" in port.lower():
            return port
    return None


def list_midi_inputs() -> list[str]:
    import mido  # imported lazily so the app still starts if the MIDI backend is broken

    return list(mido.get_input_names())


class MidiRouter:
    """Holds the latest value (0-1) of every CC seen, plus one-shot 'learn' capture."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._values: dict[tuple[int, int], float] = {}
        self._learning = False
        self._learned: MidiBinding | None = None

    def handle(self, channel: int, control: int, value: int) -> None:
        with self._lock:
            self._values[(channel, control)] = max(0, min(value, 127)) / 127.0
            if self._learning:
                self._learned = MidiBinding(channel=channel, control=control)
                self._learning = False

    def value(self, binding: MidiBinding) -> float | None:
        """Latest knob position, or None if that control hasn't been moved yet."""
        with self._lock:
            return self._values.get((binding.channel, binding.control))

    def start_learn(self) -> None:
        with self._lock:
            self._learning = True
            self._learned = None

    def cancel_learn(self) -> None:
        with self._lock:
            self._learning = False
            self._learned = None

    def pop_learned(self) -> MidiBinding | None:
        with self._lock:
            learned, self._learned = self._learned, None
            return learned


class MidiInput:
    def __init__(self, router: MidiRouter) -> None:
        self._router = router
        self._port = None

    @property
    def is_open(self) -> bool:
        return self._port is not None

    def open(self, name: str) -> None:
        import mido

        self.close()
        self._port = mido.open_input(name, callback=self._on_message)

    def close(self) -> None:
        if self._port is not None:
            try:
                self._port.close()
            finally:
                self._port = None

    def _on_message(self, message: object) -> None:  # runs on the MIDI thread
        if getattr(message, "type", None) == "control_change":
            self._router.handle(message.channel, message.control, message.value)
