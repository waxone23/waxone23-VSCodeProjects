import librosa
import numpy as np
import os
import shutil


def build_mpc_kit(directory, program_name="SmartKit"):
    output_dir = os.path.join(directory, "MPC_Ready_Kit")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = (".wav", ".aif")
    data = []

    print(f"--- Analyzing Samples in {directory} ---")

    for file in os.listdir(directory):
        if file.lower().endswith(valid_extensions):
            path = os.path.join(directory, file)
            try:
                y, sr = librosa.load(path)
                loudness = np.mean(librosa.feature.rms(y=y))
                brightness = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
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
                print(f"Error: {e}")

    if not data:
        return

    # Sort by Loudness to assign layers
    data.sort(key=lambda x: x["loudness"])
    avg_sharp = np.median([d["sharpness"] for d in data])

    # Rename and Move
    for i, entry in enumerate(data):
        if i < len(data) * 0.3:
            prefix = "GHOST_"
        elif entry["sharpness"] > (avg_sharp * 1.5):
            prefix = "SNAP_"
        else:
            prefix = "HIT_"

        new_name = prefix + entry["filename"]
        shutil.copy(entry["path"], os.path.join(output_dir, new_name))
        entry["new_name"] = new_name

    # Create XPM Program (Mapping first 4 samples to Pad 1 as an example)
    if len(data) >= 4:
        xpm_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<MPCProgram>
    <ProgramName>{program_name}</ProgramName>
    <ProgramType>Drum</ProgramType>
    <Pad>
        <Number>1</Number>
        <Layer1><SampleName>{data[0]['new_name']}</SampleName><VelStart>0</VelStart><VelEnd>32</VelEnd></Layer1>
        <Layer2><SampleName>{data[1]['new_name']}</SampleName><VelStart>33</VelStart><VelEnd>64</VelEnd></Layer2>
        <Layer3><SampleName>{data[2]['new_name']}</SampleName><VelStart>65</VelStart><VelEnd>96</VelEnd></Layer3>
        <Layer4><SampleName>{data[-1]['new_name']}</SampleName><VelStart>97</VelStart><VelEnd>127</VelEnd></Layer4>
    </Pad>
</MPCProgram>"""
        with open(os.path.join(output_dir, f"{program_name}.xpm"), "w") as f:
            f.write(xpm_content)

    print(f"--- Process Complete! Folder: {output_dir} ---")


if __name__ == "__main__":
    build_mpc_kit("./samples_folder")
