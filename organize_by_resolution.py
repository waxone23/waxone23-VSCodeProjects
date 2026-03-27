import DaVinciResolveScript as dvr_script


def organize_by_resolution():
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    clips = root_folder.GetClipList()

    for clip in clips:
        res = clip.GetClipProperty("Resolution")
        # Determine folder name
        folder_name = "4K_Clips" if "3840" in res or "4096" in res else "HD_Clips"

        # Check if folder exists, if not, create it
        target_folder = None
        for subfolder in root_folder.GetSubFolderList():
            if subfolder.GetName() == folder_name:
                target_folder = subfolder
                break

        if not target_folder:
            target_folder = media_pool.AddSubFolder(root_folder, folder_name)

        media_pool.MoveClips([clip], target_folder)
        print(f"Moved {clip.GetName()} to {folder_name}")


organize_by_resolution()
