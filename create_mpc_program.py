import os
import librosa
import numpy as np


def create_mpc_program(directory, program_name="AutoKit"):
    valid_extensions = (".wav", ".aif")
    samples = []

    # 1. Analyze and Sort
    for file in os.listdir(directory):
        if file.lower().endswith(valid_extensions):
            path = os.path.join(directory, file)
            y, sr = librosa.load(path)
            loudness = np.mean(librosa.feature.rms(y=y))
            samples.append({"name": file, "loudness": loudness})

    # Sort samples by loudness (Softest to Loudest)
    samples.sort(key=lambda x: x["loudness"])

    # We will map the top 4 samples to Pad A01 as 4 Velocity Layers
    if len(samples) < 4:
        print("Need at least 4 samples to create a full articulation layer.")
        return

    # 2. Generate XPM (XML) Content
    xpm_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<MPCProgram>
    <ProgramName>{program_name}</ProgramName>
    <ProgramType>Drum</ProgramType>
    <Pad>
        <Number>1</Number>
        <Layer1><SampleName>{samples[0]['name']}</SampleName><VelStart>0</VelStart><VelEnd>32</VelEnd></Layer1>
        <Layer2><SampleName>{samples[1]['name']}</SampleName><VelStart>33</VelStart><VelEnd>64</VelEnd></Layer2>
        <Layer3><SampleName>{samples[2]['name']}</SampleName><VelStart>65</VelStart><VelEnd>96</VelEnd></Layer3>
        <Layer4><SampleName>{samples[3]['name']}</SampleName><VelStart>97</VelStart><VelEnd>127</VelEnd></Layer4>
    </Pad>
</MPCProgram>"""

    # 3. Save the file
    with open(os.path.join(directory, f"{program_name}.xpm"), "w") as f:
        f.write(xpm_content)

    print(f"Success! {program_name}.xpm created with 4-layer velocity articulation.")


if __name__ == "__main__":
    create_mpc_program("./my_samples")
