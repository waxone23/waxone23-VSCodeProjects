# VJ Bridge User Guide

VJ Bridge connects Ableton Live audio to Resolume Avenue. It listens to a loopback audio device, analyzes the signal into frequency bands, detects kick hits, and sends the resulting values to Resolume over OSC.

## 1. What You Need

### macOS

- macOS on Apple Silicon or Intel
- Ableton Live
- Resolume Avenue
- BlackHole 2ch or another loopback audio device
- Optional: Akai APC40 MKII or another MIDI controller
- Microphone permission for VJ Bridge

### Windows

- Windows 10 or newer
- Ableton Live
- Resolume Avenue
- VB-Cable or another loopback audio device
- Optional: Akai APC40 MKII or another MIDI controller

## 2. Install the App

### Packaged macOS app

1. Open `dist/VJ Bridge.app`.
2. On the first launch, macOS may require Control-click > Open because the app is ad-hoc signed and not notarized.
3. Allow microphone access when macOS asks. BlackHole is treated as an audio input device.
4. The distributable disk image is `dist/VJ-Bridge-macos.dmg`.

### Run from source

Use Python 3.10 or newer:

```text
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_vj_bridge.py
```

On Windows, activate the environment with:

```text
.venv\Scripts\activate
```

## 3. Route Ableton Audio

VJ Bridge must receive the same audio that Ableton is playing.

### macOS with BlackHole

1. Install BlackHole 2ch.
2. Open **Audio MIDI Setup**.
3. Create a **Multi-Output Device** containing your normal speakers or headphones and BlackHole 2ch.
4. In Ableton Live, open **Settings > Audio**.
5. Choose the Multi-Output Device as the output device.
6. In VJ Bridge, choose **BlackHole 2ch** in the input device menu.

The Multi-Output Device lets you hear Ableton while BlackHole provides the signal to VJ Bridge.

### Windows with VB-Cable

1. Install VB-Cable.
2. In Ableton Live, open **Preferences > Audio**.
3. Route the master output or a dedicated bus to the VB-Cable output.
4. In VJ Bridge, choose the matching VB-Cable input, usually named `CABLE Output`.
5. Use Windows monitoring or a second Ableton output if you also need to hear the music locally.

## 4. Configure Resolume

1. Open Resolume Avenue.
2. Open **Preferences > OSC**.
3. Enable OSC input.
4. Use port `7000`, unless you choose another port.
5. Set VJ Bridge's Resolume IP and port to match. For Resolume on the same computer, use `127.0.0.1`.
6. Press **Start** in VJ Bridge.
7. Play audio in Ableton and confirm that the VJ Bridge meters move.

The default OSC addresses are examples only. Replace them with addresses from your Resolume composition before relying on the mappings in a performance.

## 5. Find Resolume OSC Addresses

1. In Resolume, enter Shortcuts edit mode.
2. Select the parameter you want to control.
3. Copy or note its OSC address.
4. In VJ Bridge, open the **Mappings** tab.
5. Paste the address into the mapping row.
6. Set the source, minimum, maximum, and curve.
7. Press **Test** on the row and watch the parameter in Resolume.

Useful parameter types include layer opacity, clip opacity, effect amount, scale, rotation, and color controls. Keep output ranges conservative until the mapping is proven.

## 6. Understand the Main Window

### Header

- **Input** selects the audio device.
- **Rescan** refreshes audio devices.
- **Resolume IP** and **Port** select the OSC destination.
- **Start** and **Stop** control the audio engine.
- The status message reports connection and audio errors.

### Levels

The meters show the current normalized values for:

- `kick`: low-frequency energy
- `bass`: low-end musical energy
- `mids`: midrange energy
- `highs`: high-frequency energy
- `kick_pulse`: a short hit signal for flashes and impacts

The history plot shows approximately the last five seconds.

### Mappings

Each row can be enabled or disabled and contains:

- **Source**: a band, `kick_pulse`, or `manual`
- **OSC address**: the Resolume parameter address
- **Min / Max**: output range
- **Curve**: response shaping; higher values make the response more selective
- **Amount**: how strongly the audio drives the parameter
- **Test**: sends a test value through the row

The mapping calculation is:

```text
output = min + (max - min) * (source_value ^ curve) * amount
```

Values are clamped to the 0 to 1 range before shaping.

### Bands

The **Bands** tab controls the frequency range and response timing for each band:

- `low_hz` and `high_hz` define the frequency range.
- `attack` controls how quickly a rising signal responds.
- `release` controls how quickly the level falls.
- Kick threshold controls how large a rise must be before a kick pulse fires.
- Kick cooldown prevents repeated triggers from one hit.

Band edits rebuild the analyzer and briefly reset the meters.

## 7. APC40 and MIDI Control

1. Put the APC40 MKII in Generic mode.
2. In Ableton's MIDI settings, set its control surface to **None**.
3. Unplug and reconnect the APC40.
4. Open the VJ Bridge **Mappings** tab.
5. Select the controller if it was not auto-selected.
6. Click **Learn...** on a mapping row.
7. Move a knob or fader.
8. Start VJ Bridge to let the controller affect the mapping.

By default, the learned control changes **Amount**:

- `0` means the music has no effect.
- `1` means the mapping receives its full audio response.

For direct manual control, choose the `manual` source. The learned control then moves the parameter between its minimum and maximum values.

Assignments are saved in presets. The current implementation does not provide soft pick-up, so a knob can jump to its physical position when first used.

On Windows, only one application can hold a MIDI port at a time. If the APC40 is reported as busy, disable its Track and Remote ports in Ableton or route it through loopMIDI.

## 8. Presets and Settings

Use the **File** menu to save, load, or reset presets.

Presets contain:

- Band ranges and response timings
- Kick threshold and cooldown
- OSC mappings
- MIDI assignments

Machine-specific settings contain:

- Selected audio device
- Resolume IP and port
- Selected MIDI device
- OSC rate
- Current preset name
- Window position and size

Files are stored here:

```text
~/.vj_bridge/settings.json
~/.vj_bridge/presets/
```

Use **File > Open presets folder** to open the preset directory.

## 9. Tuning Guide

Start with the default values and play a representative track.

1. Confirm that the meters respond without clipping at zero or one.
2. Replace placeholder OSC addresses with real Resolume addresses.
3. Adjust band ranges to match the music.
4. For a sub-heavy kick, try lowering the kick high frequency to around 80 Hz.
5. Increase release time when a meter is too nervous.
6. Decrease release time when the response feels slow.
7. Increase curve above `1.0` when only strong hits should move a parameter.
8. Use `kick_pulse` for flashes, scale hits, and strobe-like effects.
9. Use `bass`, `mids`, and `highs` for slower continuous modulation.
10. Tune kick threshold and cooldown last, after the kick band itself looks correct.

## 10. Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| Cmd+Enter on macOS / Ctrl+Enter on Windows | Start or stop |
| Cmd+S on macOS / Ctrl+S on Windows | Save preset |
| Cmd+Q on macOS / Ctrl+Q on Windows | Quit |

## 11. Troubleshooting

### The app does not hear audio

- Confirm Ableton is playing.
- Confirm Ableton is routed to the loopback device.
- Confirm VJ Bridge is using the loopback input, not the speakers or built-in microphone.
- Check macOS microphone permission in **System Settings > Privacy & Security > Microphone**.
- Try **Rescan** and select the device again.
- Avoid aggregate devices that report zero input channels.

### The meters move but Resolume does not react

- Confirm OSC input is enabled in Resolume.
- Confirm the IP and port match.
- Replace the placeholder OSC address.
- Use the mapping **Test** button.
- Temporarily map a simple opacity parameter with a `0.0` to `1.0` range.

### The signal is too quiet or always saturated

- Check Ableton's master and bus levels.
- Choose the correct loopback device.
- Adjust the band frequency range.
- Let the auto-gain settle for several seconds after starting playback.
- Check whether another application is already controlling the audio device.

### MIDI learning does not work

- Confirm the controller appears in the VJ Bridge controller menu.
- Put the APC40 in Generic mode.
- Make sure the app is started while testing the learned control.
- On Windows, close other applications using the MIDI port.
- Move a knob or fader only after clicking **Learn...**.

### The packaged app is blocked on another Mac

The app is ad-hoc signed and not notarized. Control-click the app, choose **Open**, and confirm the dialog. A notarized release requires an Apple Developer account and a signed distribution workflow.

## 12. Build and Distribute

Build the macOS app from the project folder:

```text
./build_macos.sh
```

This creates:

```text
dist/VJ Bridge.app
dist/VJ-Bridge-macos.dmg
```

The build includes the macOS icon, microphone usage description, and bundled PortAudio resources.

Build Windows on Windows with `build_windows.bat`. PyInstaller builds must be performed on the operating system being targeted.

## 13. Signal Processing Reference

The analyzer uses a 2048-sample FFT and a 512-sample hop at 48 kHz. This gives approximately 10.7 ms analysis steps and enough frequency resolution for kick and bass work.

Default bands:

| Band | Range | Default role |
| --- | --- | --- |
| Kick | 40-100 Hz | Impact and pulse detection |
| Bass | 100-250 Hz | Low-end movement |
| Mids | 250-2000 Hz | Body and musical texture |
| Highs | 6000-16000 Hz | Brightness and detail |

Each band has an envelope follower and slowly adapting auto-gain. Kick detection compares the current kick level with a slower kick average, then applies a threshold and cooldown.

## 14. Performance Checklist

Before a show:

- Open Ableton, Resolume, and VJ Bridge in the intended order.
- Confirm the loopback device is still selected.
- Confirm microphone permission is enabled.
- Test one OSC mapping.
- Test the APC40 if used.
- Load the correct preset.
- Verify that the Resolume composition is saved.
- Disable unnecessary audio applications that may claim the device.
- Keep a copy of the preset and this guide with the show project.

## 15. Project Files

- `run_vj_bridge.py`: source entry point
- `vj_bridge/`: application code
- `vj_bridge.spec`: PyInstaller configuration
- `build_macos.sh`: macOS build script
- `build_windows.bat`: Windows build script
- `assets/`: application icons
- `requirements.txt`: Python dependencies
- `README.txt`: short project overview
