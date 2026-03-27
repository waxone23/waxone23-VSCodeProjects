import DaVinciResolveScript as dvr


def validate_metadata(clip):
    """Checks if the clip meets resolution, codec, and lens requirements."""
    meta = clip.GetMetadata()

    # 1. Resolution Check
    res = clip.GetClipProperty("Resolution")
    # Resolution usually returns a string like '3840x2160'
    try:
        width = int(res.split("x")[0])
        if width < 1920:
            return False  # Below Full HD
    except:
        return False

    # 2. Codec Check
    codec = clip.GetClipProperty("Video Codec")
    if "ProRes" not in codec:
        return False

    # 3. Lens Focal Length Check
    # Note: This requires the camera to have saved metadata to the file
    focal_length_str = meta.get("Focal Length", "0").replace("mm", "").strip()
    try:
        focal_length = float(focal_length_str)
        if not (8 <= focal_length <= 200):
            return False
    except ValueError:
        # If no focal length metadata exists, decide if you want to keep or discard
        return False

    return True


def filter_resolve_media(folder_path):
    resolve = dvr.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    mp = project.GetMediaPool()

    # Create Bins
    root = mp.GetRootFolder()
    good_bin = mp.AddSubFolder(root, "Approved_Clips")
    reject_bin = mp.AddSubFolder(root, "Rejected_Clips")

    # Import all .mov files first to read their metadata
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".mov")]
    clips = mp.ImportMedia([os.path.join(folder_path, f) for f in files])

    for clip in clips:
        if validate_metadata(clip):
            mp.MoveClips([clip], good_bin)
        else:
            mp.MoveClips([clip], reject_bin)

    print("Sorting complete.")
