import DaVinciResolveScript as dvr_script


def timecode_to_frames(timecode, fps):
    """Converts 'HH:MM:SS:FF' or 'HH:MM:SS' to a total frame count."""
    parts = timecode.replace(";", ":").split(":")

    # Handle cases where frames (FF) might be missing
    while len(parts) < 4:
        parts.append("00")

    hours, minutes, seconds, frames = map(int, parts)
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return int((total_seconds * fps) + frames)


def inject_markers():
    # 1. Connect to Resolve
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()

    if not timeline:
        print("Error: No active timeline found. Please open a timeline first.")
        return

    # 2. Get the Timeline FPS (Resolve stores this as a float)
    fps = float(timeline.GetSetting("timelineFrameRate"))
    print(f"Project FPS detected: {fps}")

    # 3. Your "Data Input" - This is where your AI notes or manual list goes
    # Format: (Timecode, Color, Name, Note)
    marker_data = [
        ("00:00:05:00", "Blue", "Intro", "Start of the interview"),
        ("00:01:12:15", "Yellow", "B-Roll", "Insert landscape shot here"),
        ("00:02:45:00", "Red", "Mistake", "Subject coughed - edit out"),
        ("00:05:10:00", "Green", "Key Quote", "Everything is automated now!"),
    ]

    # 4. Process and Add
    for tc, color, name, note in marker_data:
        frame_id = timecode_to_frames(tc, fps)

        # AddMarker(frameId, color, name, note, duration)
        success = timeline.AddMarker(frame_id, color, name, note, 1)

        if success:
            print(f"✅ Added {color} marker at {tc} (Frame {frame_id})")
        else:
            print(f"❌ Failed to add marker at {tc}. Is it outside timeline bounds?")


if __name__ == "__main__":
    inject_markers()
