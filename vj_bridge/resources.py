"""Locate bundled assets, both in a source checkout and inside a PyInstaller build."""

from __future__ import annotations

import sys
from pathlib import Path


def asset_path(name: str) -> str:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return str(base / "assets" / name)
