def apply_cst_notes():
    resolve = dvr_script.scriptapp("Resolve")
    timeline = resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline()
    # Get clips from Video Track 1
    items = timeline.GetItemListInTrack("video", 1)

    for item in items:
        media_pool_item = item.GetMediaPoolItem()
        camera = media_pool_item.GetMetadata("Camera")

        if "Sony" in camera:
            item.SetShotNotes("CST: S-Log3 -> Rec.709")
            item.SetClipColor("Blue")
        elif "Blackmagic" in camera:
            item.SetShotNotes("CST: BM Film Gen 5 -> Rec.709")
            item.SetClipColor("Yellow")


apply_cst_notes()
