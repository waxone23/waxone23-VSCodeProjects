import os
import subprocess
import json

# Studio Standard Configuration
STUDIO_CODEC = "prores"
REQUIRED_RES = "3840x2160"


def audit_file(file_path):
    # Use FFprobe to get metadata
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        file_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    metadata = json.loads(result.stdout)

    # Check Video Stream
    video_stream = next(s for s in metadata["streams"] if s["codec_type"] == "video")

    codec = video_stream["codec_name"]
    width = video_stream["width"]
    height = video_stream["height"]
    resolution = f"{width}x{height}"

    # Logic Check
    if STUDIO_CODEC not in codec.lower() or resolution != REQUIRED_RES:
        print(f"❌ REJECTED: {os.path.basename(file_path)} is {codec} @ {resolution}")
        return False

    print(f"✅ PASSED: {os.path.basename(file_path)} is Studio-Ready.")
    return True


# This would run in a loop watching the 'Incoming' folder
