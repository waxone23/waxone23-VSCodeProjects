import os


def update_asset_version(asset_name, version_folder, live_folder):
    """
    Updates the 'LIVE' symbolic link to point to the highest version number.
    """
    # Get all versions of the specific asset
    all_files = [f for f in os.listdir(version_folder) if f.startswith(asset_name)]
    if not all_files:
        print(f"No versions found for {asset_name}")
        return

    # Sort to find the latest (e.g., v003 > v002)
    all_files.sort()
    latest_version = all_files[-1]

    full_latest_path = os.path.join(version_folder, latest_version)
    live_link_path = os.path.join(live_folder, f"{asset_name}_LIVE.mov")

    # Remove old link if it exists
    if os.path.exists(live_link_path):
        os.remove(live_link_path)

    # Create the new symbolic link (Requires Admin/Developer mode on Windows)
    try:
        os.symlink(full_latest_path, live_link_path)
        print(f"✅ Success: {asset_name}_LIVE now points to {latest_version}")
    except OSError as e:
        print(f"❌ Failed to create link: {e}")


# --- Example Usage for Try Studio ---
# update_asset_version("Nike_Commercial_Edit", "Z:/Projects/Nike/Versions", "Z:/Projects/Nike/Edit")
