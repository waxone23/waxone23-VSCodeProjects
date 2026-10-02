VJ BRIDGE 0.3 - audio-reactive link between Ableton Live and Resolume Avenue
============================================================================

RUN FROM SOURCE (Python 3.10+)
  python -m venv .venv
  .venv\Scripts\activate          (Windows)    or    source .venv/bin/activate   (macOS)
  pip install -r requirements.txt
  python run_vj_bridge.py
  
FULL DOCUMENTATION
  See USER_GUIDE.md for installation, Ableton routing, Resolume OSC setup,
  MIDI control, presets, tuning, troubleshooting, and show-day checklists.

BUILD A REAL APP (icon, no terminal window)
  PyInstaller cannot cross-compile, so build on the OS you want to ship for.

  Windows:  double-click build_windows.bat
            -> dist\VJ Bridge\VJ Bridge.exe   and   dist\VJ-Bridge-windows.zip
  macOS:    ./build_macos.sh
            -> dist/VJ Bridge.app   and   dist/VJ-Bridge-macos.dmg

  macOS notes:
    - The build adds the microphone permission text macOS requires for audio
      input (BlackHole counts as a microphone). Without it the app hears nothing.
    - The app is ad-hoc signed, not notarized. On another Mac: right-click the
      app > Open the first time. Notarizing needs an Apple Developer account.
  Windows notes:
    - Unsigned apps may show a SmartScreen warning: More info > Run anyway.

FIRST LAUNCH
  A setup guide opens automatically (reopen via Help > Setup guide).
  Short version: route Ableton's output to a loopback device (BlackHole on
  macOS, VB-Cable on Windows), enable OSC input in Resolume (port 7000), pick
  the loopback device as Input, press Start, then set real OSC addresses in the
  Mappings tab.

APC40 / MIDI KNOB CONTROL
  1. Put the APC40 MKII in Generic mode: in Ableton's MIDI settings set its
     control surface to None, then unplug and replug the controller.
     (Live otherwise switches it into Ableton mode.)
  2. Mappings tab > Controller: pick the APC40 (picked automatically if found).
  3. Click "Learn..." on a mapping row, then move any knob or fader. That
     control now sets the row's Amount (0 = sound has no effect, 1 = full
     effect) live. "Unassign knob" removes it. Assignments are saved in presets.
  4. For direct manual control of a parameter, set the row's Source to
     "manual": the knob then sets the parameter between Min and Max.
  Notes:
    - Knobs only act while VJ Bridge is started.
    - On Windows a MIDI port can be opened by only one app at a time. If the
      APC is "in use", disable its Track/Remote ports in Ableton (and don't
      map it directly in Resolume), or route it through loopMIDI.
    - A knob jumps straight to its physical position (no soft pick-up yet).

SHORTCUTS
  Ctrl+Enter  start / stop          Ctrl+S  save preset          Ctrl+Q  quit
  (Cmd instead of Ctrl on macOS)

WHERE THINGS ARE SAVED
  ~/.vj_bridge/settings.json   device, Resolume address, current preset
  ~/.vj_bridge/presets/        saved presets (File > Open presets folder)
  Window size/position is remembered automatically.

PROJECT LAYOUT
  run_vj_bridge.py       entry point (source and PyInstaller)
  vj_bridge.spec         PyInstaller config (icon, mic permission, bundled PortAudio)
  build_windows.bat / build_macos.sh
  assets/                icon.png, icon.ico, icon.icns
  tools/make_icon.py     regenerates the icons (needs Pillow)
  vj_bridge/             config, audio, osc_out, midi_in, engine, theme, resources, ui
