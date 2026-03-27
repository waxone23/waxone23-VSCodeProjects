"""
MPC ONE DRUM ARTICULATION FEATURE ANALYZER
------------------------------------------
Requirements: pip install librosa scikit-learn numpy
Instructions:
1. Place your drum samples in a folder.
2. Update the 'folder_path' variable at the bottom of this script.
3. Run the script to identify the most relevant features for your kit.
"""

import librosa
import numpy as np
import os
from sklearn.feature_selection import VarianceThreshold


def analyze_drum_kit(directory):
    print(f"--- Starting Analysis in: {directory} ---")
    feature_list = []
    file_names = []

    # Supported audio formats
    valid_extensions = (".wav", ".aif", ".mp3")

    for file in os.listdir(directory):
        if file.lower().endswith(valid_extensions):
            path = os.path.join(directory, file)
            try:
                # Load audio
                y, sr = librosa.load(path)

                # Feature 1: Brightness (Spectral Centroid)
                # High brightness = Good for Accents
                brightness = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

                # Feature 2: Loudness (RMS)
                # High RMS = High Velocity hits
                loudness = np.mean(librosa.feature.rms(y=y))

                # Feature 3: Timbre (MFCCs)
                # Fingerprint of the drum texture
                mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5)
                mfccs_mean = np.mean(mfccs, axis=1)

                # Feature 4: Perceived Sharpness (Zero Crossing Rate)
                # Useful for snare snap vs. ghost notes
                zcr = np.mean(librosa.feature.zero_crossing_rate(y))

                # Combine into one vector
                features = [brightness, loudness, zcr] + mfccs_mean.tolist()
                feature_list.append(features)
                file_names.append(file)
                print(f"Analyzed: {file}")
            except Exception as e:
                print(f"Error processing {file}: {e}")

    if not feature_list:
        print("No audio files found.")
        return

    # Convert to Numpy Array
    X = np.array(feature_list)

    # Feature Selection: Remove features that don't change much
    # A low threshold (e.g., 0.1) removes features that are nearly identical across samples
    selector = VarianceThreshold(threshold=0.1)

    try:
        X_selected = selector.fit_transform(X)
        relevant_indices = selector.get_support(indices=True)

        feature_names = ["Brightness", "Loudness", "ZeroCrossing"] + [
            f"MFCC_{i}" for i in range(1, 6)
        ]
        selected_names = [feature_names[i] for i in relevant_indices]

        print("\n--- RESULTS ---")
        print(f"Total Samples Analyzed: {len(file_names)}")
        print(
            f"Most Relevant Features for your Articulations: {', '.join(selected_names)}"
        )
        print("Use these high-variance features to map your MPC Articulation slots.")

    except ValueError:
        print(
            "\n[Error] Not enough variance found. Your samples might be too similar for automated selection."
        )


if __name__ == "__main__":
    # CHANGE THIS to your folder path
    folder_path = "./my_drum_samples"
    analyze_drum_kit(folder_path)
