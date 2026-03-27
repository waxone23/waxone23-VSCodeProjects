import librosa
import numpy as np
import os


def analyze_hi_hat_type(y, sr):
    # Calculate Spectral Roll-off (85% energy threshold)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)[0]

    # Analyze the decay of the brightness
    # Closed hats lose high-end energy almost instantly.
    start_energy = np.mean(rolloff[:5])
    end_energy = np.mean(rolloff[10:15]) if len(rolloff) > 15 else 0

    decay_ratio = end_energy / start_energy if start_energy > 0 else 0

    if decay_ratio < 0.3:
        return "CHOKE/CLOSED"
    elif decay_ratio > 0.7:
        return "OPEN"
    else:
        return "MID-DECAY"


# --- EXECUTION LOGIC ---
filename = "hihat.wav"  # <-- Change this to your actual file name!

if os.path.exists(filename):
    print(f"Analyzing {filename}...")
    y, sr = librosa.load(filename)
    result = analyze_hi_hat_type(y, sr)
    print(f"Detected Type: {result}")
else:
    print(f"Error: Could not find '{filename}' in this folder.")
