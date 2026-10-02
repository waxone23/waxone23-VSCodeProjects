#!/usr/bin/env bash
# Builds "dist/VJ Bridge.app" and a .dmg you can share. Run from this folder.
set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv-build
source .venv-build/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --clean vj_bridge.spec

# Ad-hoc sign so Apple Silicon Macs will launch it (not the same as notarization).
codesign --force --deep --sign - "dist/VJ Bridge.app"

rm -f "dist/VJ-Bridge-macos.dmg"
hdiutil create -volname "VJ Bridge" -srcfolder "dist/VJ Bridge.app" -ov -format UDZO "dist/VJ-Bridge-macos.dmg"

echo
echo "Done:  dist/VJ Bridge.app"
echo "Share: dist/VJ-Bridge-macos.dmg"
echo "First launch on another Mac: right-click the app > Open (it is not notarized)."
