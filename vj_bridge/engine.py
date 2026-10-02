"""Engine: audio stream -> Analyzer -> mappings -> OSC, running off the UI thread."""

from __future__ import annotations

import threading
import time

import numpy as np
import sounddevice as sd

from .audio import HOP, Analyzer, resolve_device
from .config import MANUAL, Settings
from .midi_in import MidiRouter
from .osc_out import OscSender


class Engine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.analyzer: Analyzer | None = None
        self.osc = OscSender(settings.resolume_ip, settings.resolume_port)
        self.midi = MidiRouter()  # latest knob positions; fed by the MIDI input
        self._stream: sd.InputStream | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    # --- state ---

    @property
    def running(self) -> bool:
        return self._stream is not None

    @property
    def healthy(self) -> bool:
        return self._stream is not None and self._stream.active

    def snapshot(self) -> dict[str, float]:
        analyzer = self.analyzer
        values = dict(analyzer.values) if analyzer else {}
        values[MANUAL] = 1.0
        return values

    def input_level(self) -> float:
        analyzer = self.analyzer
        return analyzer.input_level if analyzer else 0.0

    # --- lifecycle ---

    def start(self) -> str:
        """Open the audio stream and start sending. Returns the device name in use."""
        if self.running:
            return ""
        index = resolve_device(self.settings.device)
        if index is None:
            index = sd.default.device[0]
        if index is None or index < 0:
            raise RuntimeError("No audio input device available.")

        info = sd.query_devices(index)
        sample_rate = int(info["default_samplerate"])
        channels = max(1, min(2, int(info["max_input_channels"])))
        preset = self.settings.preset

        self.analyzer = Analyzer(preset.bands, sample_rate, preset.onset_threshold, preset.onset_cooldown)
        self._stream = sd.InputStream(
            device=index,
            channels=channels,
            samplerate=sample_rate,
            blocksize=HOP,
            dtype="float32",
            callback=self._callback,
        )
        try:
            self._stream.start()
        except Exception:
            self._stream.close()
            self._stream = None
            raise

        self._stop.clear()
        self._thread = threading.Thread(target=self._send_loop, name="osc-sender", daemon=True)
        self._thread.start()
        return str(info["name"])

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            finally:
                self._stream = None

    # --- live updates (safe while running) ---

    def rebuild_analyzer(self) -> None:
        """Call after band edits. Swaps in a fresh analyzer; the audio callback picks it up."""
        if self.analyzer is None:
            return
        preset = self.settings.preset
        self.analyzer = Analyzer(
            preset.bands, self.analyzer.sample_rate, preset.onset_threshold, preset.onset_cooldown
        )

    def update_onset(self) -> None:
        if self.analyzer is not None:
            preset = self.settings.preset
            self.analyzer.onset_threshold = preset.onset_threshold
            self.analyzer.onset_cooldown = preset.onset_cooldown

    # --- internals ---

    def _callback(self, indata: np.ndarray, frames: int, time_info: object, status: sd.CallbackFlags) -> None:
        analyzer = self.analyzer
        if analyzer is not None:
            analyzer.process(indata.mean(axis=1))

    def _send_loop(self) -> None:
        while not self._stop.is_set():
            started = time.monotonic()
            settings = self.settings
            self.osc.set_target(settings.resolume_ip, settings.resolume_port)
            values = self.snapshot()
            for mapping in list(settings.preset.mappings):
                if not mapping.enabled or not mapping.address.startswith("/"):
                    continue
                if mapping.source in values:
                    knob = self.midi.value(mapping.knob) if mapping.knob is not None else None
                    self.osc.send_if_changed(mapping.address, mapping.apply(values[mapping.source], knob))
            interval = 1.0 / max(settings.osc_rate_hz, 1)
            time.sleep(max(0.0, interval - (time.monotonic() - started)))
