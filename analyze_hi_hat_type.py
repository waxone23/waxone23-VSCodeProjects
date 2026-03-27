import librosa
import numpy as np


def analyze_hi_hat_type(y, sr):
    # Calculate Spectral Roll-off
    #
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)[0]

    # Calculate energy drop
    start_energy = np.mean(rolloff[:5])
    end_energy = np.mean(rolloff[10:15]) if len(rolloff) > 15 else 0

    decay_ratio = end_energy / start_energy if start_energy > 0 else 0

    if decay_ratio < 0.3:
        return "CHOKE_"
    elif decay_ratio > 0.7:
        return "OPEN_"
    else:
        return "CLOSED_"


# Example of how to actually trigger the function:
# audio_path = "path/to/your/hihat.wav"
# y, sr = librosa.load(audio_path)
# print(analyze_hi_hat_type(y, sr))
