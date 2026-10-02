"""Pydantic models for settings and presets, plus persistence to disk.

Two layers:
- Preset:   what the music drives (bands, mappings, onset tuning). Shareable files.
- Settings: machine-level stuff (audio device, Resolume address) + the current preset.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

CONFIG_DIR = Path.home() / ".vj_bridge"
PRESET_DIR = CONFIG_DIR / "presets"
SETTINGS_PATH = CONFIG_DIR / "settings.json"

KICK_PULSE = "kick_pulse"  # virtual source produced by onset detection
MANUAL = "manual"  # virtual source that is always 1.0, so a knob controls the parameter directly


class Band(BaseModel):
    name: str
    low_hz: float
    high_hz: float
    attack: float = 0.01  # seconds
    release: float = 0.15  # seconds


class MidiBinding(BaseModel):
    channel: int  # 0-15
    control: int  # CC number 0-127

    def label(self) -> str:
        return f"Ch{self.channel + 1} · CC{self.control}"


class Mapping(BaseModel):
    enabled: bool = True
    source: str  # a band name, or KICK_PULSE
    address: str  # Resolume OSC address
    out_min: float = 0.0
    out_max: float = 1.0
    curve: float = 1.0  # >1 = snappier, only big hits get through
    amount: float = 1.0  # 0-1 depth of the effect; a bound knob overrides this live
    knob: MidiBinding | None = None  # MIDI CC that controls `amount`

    def apply(self, value: float, amount: float | None = None) -> float:
        depth = self.amount if amount is None else amount
        shaped = max(0.0, min(value, 1.0)) ** self.curve * max(0.0, min(depth, 1.0))
        return self.out_min + (self.out_max - self.out_min) * shaped


def default_bands() -> list[Band]:
    return [
        Band(name="kick", low_hz=40, high_hz=100, attack=0.005, release=0.12),
        Band(name="bass", low_hz=100, high_hz=250, attack=0.010, release=0.20),
        Band(name="mids", low_hz=250, high_hz=2000, attack=0.010, release=0.15),
        Band(name="highs", low_hz=6000, high_hz=16000, attack=0.003, release=0.08),
    ]


def default_mappings() -> list[Mapping]:
    # Placeholder addresses: replace with ones copied from Resolume.
    return [
        Mapping(source=KICK_PULSE, address="/composition/layers/1/video/opacity", out_min=0.6, out_max=1.0),
        Mapping(source="bass", address="/composition/layers/2/video/opacity", curve=1.5),
        Mapping(source="highs", address="/composition/layers/3/video/opacity", curve=2.0),
    ]


class Preset(BaseModel):
    bands: list[Band] = Field(default_factory=default_bands)
    mappings: list[Mapping] = Field(default_factory=default_mappings)
    onset_threshold: float = 0.25
    onset_cooldown: float = 0.15  # seconds


class Settings(BaseModel):
    device: str | None = None  # device label, None = system default
    resolume_ip: str = "127.0.0.1"
    resolume_port: int = 7000
    midi_device: str | None = None  # None = never chosen (auto-detect APC40); "__none__" = chosen "None"
    osc_rate_hz: int = 60
    preset_name: str | None = None  # name of the preset file last loaded/saved
    first_run_done: bool = False  # setup guide shown once on first launch
    preset: Preset = Field(default_factory=Preset)


def load_settings() -> Settings:
    try:
        return Settings.model_validate_json(SETTINGS_PATH.read_text())
    except (FileNotFoundError, ValueError):
        return Settings()


def save_settings(settings: Settings) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(settings.model_dump_json(indent=2))
