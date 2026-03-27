import os
import subprocess


def create_proxies(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):
        if file.endswith((".mp4", ".mov", ".mxf")):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, f"proxy_{file}")

            # FFmpeg command for ProRes Proxy
            cmd = [
                "ffmpeg",
                "-i",
                input_path,
                "-c:v",
                "prores_ks",
                "-profile:v",
                "0",
                "-s",
                "1280x720",
                "-c:a",
                "copy",
                output_path,
            ]

            print(f"Processing: {file}")
            subprocess.run(cmd)


# Example usage:
# create_proxies("C:/Footage/RAW", "C:/Footage/Proxies")
