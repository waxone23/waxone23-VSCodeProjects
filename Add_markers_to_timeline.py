import DaVinciResolveScript as dvr_script


def add_markers_to_timeline():
    # Connect to Resolve
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()

    if not timeline:
        print("No active timeline found!")
        return

    # Define your marker data (Frame Number, Color, Name, Note, Duration)
    # Note: 24fps project: 24 frames = 1 second.
    marker_list = [
        (24, "Blue", "Action Starts", "The subject enters the frame", 1),
        (120, "Red", "Audio Peak", "Check volume levels here", 5),
        (240, "Green", "Key Keyword", "Transcription: 'Innovation'", 1),
    ]

    print(f"Adding markers to timeline: {timeline.GetName()}")

    for frame, color, name, note, duration in marker_list:
        # AddMarker(frameId, color, name, note, duration)
        success = timeline.AddMarker(frame, color, name, note, duration)

        if success:
            print(f"✅ Added {color} marker at frame {frame}")
        else:
            print(f"❌ Failed to add marker at frame {frame}")


if __name__ == "__main__":
    add_markers_to_timeline()
