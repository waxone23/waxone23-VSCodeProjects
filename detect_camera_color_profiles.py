import DaVinciResolveScript as dvr_script


def get_grading_suggestion(camera, profile):
    """Returns a basic treatment suggestion based on camera type."""
    camera = camera.lower()

    if "sony" in camera:
        return "Treatment: Use Color Space Transform (CST) from S-Gamut3.Cine/S-Log3 to Rec.709. Add slight magenta tint in offset to balance Sony greens."
    elif "blackmagic" in camera:
        return "Treatment: Set Gamma to Blackmagic Design Film. Use the HDR Palettes for 'Zone' based exposure adjustments."
    elif "canon" in camera:
        return "Treatment: Apply C-Log to Rec.709 LUT. Canon skin tones are great; keep saturation moderate in the shadows."
    elif "arri" in camera:
        return "Treatment: Use the classic ARRI LogC to Rec709 3D LUT. Focus on subtle contrast in the mid-tones."
    else:
        return "Treatment: Standard Rec.709 normalization. Check waveform for clipping."


def analyze_clips():
    resolve = dvr_script.scriptapp("Resolve")
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    clips = root_folder.GetClipList()

    print(f"--- Analyzing {len(clips)} clips ---\n")

    for clip in clips:
        # Fetching metadata
        name = clip.GetClipProperty("File Name")
        camera = clip.GetMetadata("Camera") or "Unknown Camera"

        # 'Usage' or 'Notes' often contain profile info if not explicitly set
        profile = clip.GetMetadata("Color Space") or "Auto/Unknown"

        suggestion = get_grading_suggestion(camera, profile)

        print(f"FILE: {name}")
        print(f"CAMERA: {camera}")
        print(f"PROFILE: {profile}")
        print(f"SUGGESTION: {suggestion}")
        print("-" * 30)


if __name__ == "__main__":
    analyze_clips()
