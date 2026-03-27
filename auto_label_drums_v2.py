"""
MPC ONE ULTIMATE AUTO-LABELER
---------------------------------------
Categorizes samples by:
1. Loudness (RMS) -> GHOST, MED, HARD
2. Brightness (Centroid) -> DARK vs BRIGHT
3. Sharpness (ZCR) -> SNAP (for Flams/Rimshots)
"""

import librosa
import numpy as np
import os
import shutil


def auto_label_drums_v2(directory):
    output_dir = os.path.join(directory, "MPC_Categorized_Kit")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = (".wav", ".aif")
    data = []

    print(f"--- Analyzing {directory} ---")

    for file in os.listdir(directory):
        if file.lower().endswith(valid_extensions):
            path = os.path.join(directory, file)
            try:
                y, sr = librosa.load(path)

                # Extract Features
                loudness = np.mean(librosa.feature.rms(y=y))
                brightness = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
                # Zero Crossing Rate measures 'snap' or high-frequency transients
                sharpness = np.mean(librosa.feature.zero_crossing_rate(y))

                data.append(
                    {
                        "filename": file,
                        "path": path,
                        "loudness": loudness,
                        "brightness": brightness,
                        "sharpness": sharpness,
                    }
                )
            except Exception as e:
                print(f"Skipping {file}: {e}")

    if not data:
        return

    # Calculate Medians for comparison
    avg_loud = np.median([d["loudness"] for d in data])
    avg_sharp = np.median([d["sharpness"] for d in data])

    for entry in data:
        # 1. Determine Articulation Prefix
        if entry["loudness"] < (avg_loud * 0.7):
            prefix = "GHOST_"
        elif entry["sharpness"] > (avg_sharp * 1.5):
            prefix = "SNAP_ACCENT_"  # High transient snap
        elif entry["loudness"] > (avg_loud * 1.3):
            prefix = "HARD_"
        else:
            prefix = "MED_"

        # 2. Add Brightness Tag
        b_tag = (
            "BRIGHT_"
            if entry["brightness"] > np.median([d["brightness"] for d in data])
            else "WARM_"
        )

        new_name = f"{prefix}{b_tag}{entry['filename']}"
        shutil.copy(entry["path"], os.path.join(output_dir, new_name))
        print(f"Created: {new_name}")

    print(f"\nSuccess! Files moved to: {output_dir}")


if __name__ == "__main__":
    # SET YOUR FOLDER PATH HERE
    target_folder = "./my_samples"
    auto_label_drums_v2(target_folder)
