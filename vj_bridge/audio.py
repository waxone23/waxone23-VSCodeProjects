"""Audio analysis (FFT bands, envelopes, auto-gain, kick onset) and device helpers."""

from __future__ import annotations

import math
import time

import numpy as np

from .config import KICK_PULSE, Band

HOP = 512  # samples per analysis step
WINDOW = 2048  # FFT size; needed to resolve kick/bass frequencies


class Analyzer:
    def __init__(
        self,
        bands: list[Band],
        sample_rate: int,
        onset_threshold: float = 0.25,
        onset_cooldown: float = 0.15,
    ) -> None:
        dt = HOP / sample_rate
        freqs = np.fft.rfftfreq(WINDOW, 1 / sample_rate)
        self.sample_rate = sample_rate
        self.bands = bands
        self.onset_threshold = onset_threshold
        self.onset_cooldown = onset_cooldown
        self.window = np.hanning(WINDOW).astype(np.float32)
        self.masks = [(freqs >= b.low_hz) & (freqs < b.high_hz) for b in bands]
        self.coefs = {
            b.name: (math.exp(-dt / max(b.attack, 1e-4)), math.exp(-dt / max(b.release, 1e-4)))
            for b in bands
        }
        self.buffer = np.zeros(WINDOW, dtype=np.float32)
        self.env = {b.name: 0.0 for b in bands}
        self.peak = {b.name: 1.0 for b in bands}
        self.values: dict[str, float] = {b.name: 0.0 for b in bands}
        self.values[KICK_PULSE] = 0.0
        self.slow_kick = 0.0
        self.last_onset = -1e9
        self.input_level = 0.0  # block RMS, used for the "no signal" hint
        self.pulse_decay = math.exp(-dt / 0.15)
        self.peak_decay = 0.9995  # auto-gain forgets loud moments over ~20 s

    def process(self, block: np.ndarray, now: float | None = None) -> None:
        n = len(block)
        self.input_level = float(np.sqrt(np.mean(np.square(block)))) if n else 0.0
        self.buffer = np.roll(self.buffer, -n)
        self.buffer[-n:] = block
        spectrum = np.abs(np.fft.rfft(self.buffer * self.window))

        for band, mask in zip(self.bands, self.masks):
            level = float(np.sqrt(np.mean(spectrum[mask] ** 2))) if mask.any() else 0.0
            attack, release = self.coefs[band.name]
            coef = attack if level > self.env[band.name] else release
            self.env[band.name] = coef * self.env[band.name] + (1 - coef) * level
            # Floor of 1.0 stops silence from being boosted to full scale.
            self.peak[band.name] = max(
                self.env[band.name], self.peak[band.name] * self.peak_decay, 1.0
            )
            self.values[band.name] = min(self.env[band.name] / self.peak[band.name], 1.0)

        self._detect_kick(time.monotonic() if now is None else now)

    def _detect_kick(self, now: float) -> None:
        kick = self.values.get("kick", 0.0)
        if kick - self.slow_kick > self.onset_threshold and now - self.last_onset > self.onset_cooldown:
            self.values[KICK_PULSE] = 1.0
            self.last_onset = now
        else:
            self.values[KICK_PULSE] *= self.pulse_decay
        self.slow_kick = 0.9 * self.slow_kick + 0.1 * kick


# --- device helpers (sounddevice imported lazily so the DSP is testable without PortAudio) ---


def _label(info: dict) -> str:
    import sounddevice as sd

    api = sd.query_hostapis(info["hostapi"])["name"]
    return f'{info["name"]} [{api}]'


def list_input_devices() -> list[tuple[int, str]]:
    import sounddevice as sd

    return [(i, _label(d)) for i, d in enumerate(sd.query_devices()) if d["max_input_channels"] > 0]


def resolve_device(label: str | None) -> int | None:
    """Device label -> index. None if unset or the device is gone (caller falls back to default)."""
    if not label:
        return None
    for index, candidate in list_input_devices():
        if candidate == label:
            return index
    return None
