# -*- mode: python ; coding: utf-8 -*-
# Build with:  pyinstaller --noconfirm --clean vj_bridge.spec
# PyInstaller cannot cross-compile: build on Windows for Windows, on macOS for macOS.
import sys

from PyInstaller.utils.hooks import collect_data_files

APP_NAME = "VJ Bridge"
VERSION = "0.3.0"
IS_MAC = sys.platform == "darwin"
IS_WIN = sys.platform == "win32"

datas = [("assets/icon.png", "assets")]
try:  # bundled PortAudio library shipped with the sounddevice wheel (Windows/macOS)
    datas += collect_data_files("_sounddevice_data")
except Exception:
    pass

a = Analysis(
    ["run_vj_bridge.py"],
    pathex=["."],
    datas=datas,
    hiddenimports=["mido.backends.rtmidi"],  # mido loads its backend dynamically
    excludes=["tkinter", "matplotlib", "scipy", "PIL"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    console=False,  # no terminal window
    icon="assets/icon.ico" if IS_WIN else None,
)
coll = COLLECT(exe, a.binaries, a.datas, name=APP_NAME)

if IS_MAC:
    app = BUNDLE(
        coll,
        name=f"{APP_NAME}.app",
        icon="assets/icon.icns",
        bundle_identifier="com.vjbridge.app",
        version=VERSION,
        info_plist={
            "CFBundleDisplayName": APP_NAME,
            "CFBundleShortVersionString": VERSION,
            "NSHighResolutionCapable": True,
            # Without this key macOS silently gives the app no audio input at all.
            "NSMicrophoneUsageDescription": "VJ Bridge listens to your loopback audio device "
            "(e.g. BlackHole) to drive visuals in Resolume.",
        },
    )
