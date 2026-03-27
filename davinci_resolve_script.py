import os
import DaVinciResolveScript as dvr


def get_resolve():
    resolve = dvr.scriptapp("Resolve")
    return resolve


def is_clip_suitable(file_path):
    """
    PLACEHOLDER LOGIC: Define what 'suitable' means here.
    Example: Only files over 50MB and recorded in 4K.
    """
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    # Simple logic: Must be a .mov and larger than 10MB
    if file_path.lower().endswith(".mov") and file_size_mb > 10:
        return True
    return False


def sort_clips(folder_path):
    resolve = get_resolve()
    if not resolve:
        print("Error: Could not connect to DaVinci Resolve. Is it open?")
        return

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    # Create a 'Suitable Clips' bin if it doesn't exist
    target_bin = None
    for folder in root_folder.GetSubFolderList():
        if folder.GetName() == "Suitable_Clips":
            target_bin = folder
            break

    if not target_bin:
        target_bin = media_pool.AddSubFolder(root_folder, "Suitable_Clips")

    # Iterate through the files
    files_to_import = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if is_clip_suitable(full_path):
            print(f"MATCHED: {filename}")
            files_to_import.append(full_path)
        else:
            print(f"REJECTED: {filename}")

    # Import the winners into the specific bin
    media_pool.SetCurrentFolder(target_bin)
    media_pool.ImportMedia(files_to_import)
    print(f"Successfully imported {len(files_to_import)} clips.")


# RUN THE SCRIPT
# Replace with your actual directory path
my_folder = "/Users/YourName/Videos/SourceClips"
sort_clips(my_folder)
