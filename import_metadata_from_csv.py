import DaVinciResolveScript as dvr_script
import csv
import os


def import_metadata_from_csv(csv_path):
    # Connect to Resolve
    resolve = dvr_script.scriptapp("Resolve")
    project = resolve.GetProjectManager().GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    clips = root_folder.GetClipList()

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading metadata from: {csv_path}")

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Create a dictionary of CSV data for fast lookup
        # Key: FileName, Value: Metadata Dictionary
        metadata_map = {row["FileName"]: row for row in reader}

    count = 0
    for clip in clips:
        clip_name = clip.GetClipProperty("File Name")

        if clip_name in metadata_map:
            data = metadata_map[clip_name]

            # Apply metadata to standard Resolve fields
            if "Scene" in data:
                clip.SetMetadata("Scene", data["Scene"])
            if "Take" in data:
                clip.SetMetadata("Take", data["Take"])
            if "Comments" in data:
                clip.SetMetadata("Comments", data["Comments"])

            print(f"✅ Updated: {clip_name}")
            count += 1

    print(f"\nFinished! Updated {count} clips.")


# --- Execution ---
# Update this path to where your CSV is located
csv_file_path = r"C:\Path\To\Your\metadata.csv"
import_metadata_from_csv(csv_file_path)
