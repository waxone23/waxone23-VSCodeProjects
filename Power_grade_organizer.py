import DaVinciResolveScript as dvr_script


def setup_cinematic_pipeline():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline()

    if not timeline:
        print("Please open a timeline first!")
        return

    # Define our Teal & Orange Pipeline stages
    # Node 1: Exposure | Node 2: Balance | Node 3: Teal/Orange Look | Node 4: CST

    items = timeline.GetItemListInTrack("video", 1)

    for item in items:
        mp_item = item.GetMediaPoolItem()
        cam = mp_item.GetMetadata("Camera")

        # Automatic Normalization Logic
        if "Sony" in cam:
            normalization = "S-Log3 to Rec.709"
            item.SetClipColor("Blue")  # Mark Sony clips
        elif "Blackmagic" in cam:
            normalization = "BM Gen5 to Rec.709"
            item.SetClipColor("Yellow")
        else:
            normalization = "Standard Rec.709"

        # Inject the instruction into the Shot Notes
        # This acts as a manual for you when you start the Master Look
        note = f"PIPELINE: [1.Exposure] -> [2.Balance] -> [3.TEAL_ORANGE] -> [4.CST: {normalization}]"
        item.SetShotNotes(note)

    print("Pipeline instructions injected into all clips.")


setup_cinematic_pipeline()
