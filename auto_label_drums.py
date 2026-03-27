"""
MPC ONE AUTO-LABELER & FEATURE ANALYZER
---------------------------------------
This script analyzes drum samples and renames them based on
sonic characteristics for easy MPC Articulation mapping.
"""

import librosa
import numpy as np
import os
import shutil


def auto_label_drums(directory):
    print(f"--- Processing Samples in: {directory} ---")

    # Create an 'output' folder to keep your originals safe
    output_dir = os.path.join(directory, "MPC_Ready_Kits")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = (".wav", ".aif")
    data = []

    # 1. First Pass: Analyze all files
    for file in os.listdir(directory):
        if file.lower().endswith(valid_extensions):
            path = os.path.join(directory, file)
            try:
                y, sr = librosa.load(path)
                # Feature Extraction
                loudness = np.mean(librosa.feature.rms(y=y))
                brightness = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
                data.append(
                    {
                        "filename": file,
                        "path": path,
                        "loudness": loudness,
                        "brightness": brightness,
                    }
                )
            except Exception as e:
                print(f"Skipping {file}: {e}")

    if not data:
        print("No valid audio files found.")
        return

    # 2. Sort by Loudness to determine Articulation Tier
    data.sort(key=lambda x: x["loudness"])

    num_files = len(data)
    for i, entry in enumerate(data):
        # Categorize based on volume percentile
        if i < num_files * 0.33:
            prefix = "GHOST_"  # Softest hits
        elif i < num_files * 0.66:
            prefix = "MED_"  # Standard hits
        else:
            # Check if it's also very bright
            prefix = (
                "ACCENT_"
                if entry["brightness"] > np.median([d["brightness"] for d in data])
                else "HARD_"
            )

        # 3. Copy and Rename
        new_name = prefix + entry["filename"]
        shutil.copy(entry["path"], os.path.join(output_dir, new_name))
        print(f"Labeled: {new_name}")

    print(f"\n--- Done! Check the folder: {output_dir} ---")


if __name__ == "__main__":
    # Update this to your folder
    my_folder = "./my_samples"
    auto_label_drums(my_folder)
