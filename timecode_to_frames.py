def timecode_to_frames(timecode, fps):
    """
    Converts 'HH:MM:SS:FF' to a total frame count.
    Example: '00:01:10:12' at 24fps
    """
    # Split the string by the colon
    parts = timecode.split(":")

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    frames = int(parts[3])

    # Calculate total frames
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    total_frames = (total_seconds * fps) + frames

    return int(total_frames)


# --- How to use it with Resolve ---
fps_setting = 24  # Change this to match your timeline (e.g., 23.976, 30, 60)
my_timecode = "00:02:15:00"

target_frame = timecode_to_frames(my_timecode, fps_setting)
print(f"The marker should be placed at frame: {target_frame}")
