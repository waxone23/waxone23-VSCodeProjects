import os
import hashlib
import shutil

# --- CONFIGURATION ---
# Set this to True to see what would happen.
# Set this to False to actually move the files.
DRY_RUN = True


def calculate_hash(filename):
    """Generate an MD5 hash for a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except (OSError, PermissionError):
        return None
    return hash_md5.hexdigest()


def archive_duplicates(target_folder):
    trash_dir = os.path.join(target_folder, "duplicates_trash")

    if not DRY_RUN and not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    hashes = {}
    count = 0

    print(
        f"--- {'DRY RUN ACTIVE (No files will be moved)' if DRY_RUN else 'REAL MODE (Moving files...)'} ---"
    )

    for root, dirs, files in os.walk(target_folder):
        if "duplicates_trash" in root:
            continue

        for file_name in files:
            full_path = os.path.join(root, file_name)
            file_hash = calculate_hash(full_path)

            if file_hash:
                if file_hash in hashes:
                    count += 1
                    if DRY_RUN:
                        print(f"[WOULD MOVE] {full_path} -> to trash")
                    else:
                        dest_path = os.path.join(trash_dir, f"copy_{count}_{file_name}")
                        shutil.move(full_path, dest_path)
                        print(f"[MOVED] {file_name}")
                else:
                    hashes[file_hash] = full_path

    status = "found (dry run)" if DRY_RUN else "moved"
    print(f"\nTotal duplicates {status}: {count}")
    if DRY_RUN and count > 0:
        print(
            "To actually move these files, change 'DRY_RUN = True' to 'DRY_RUN = False' in the code."
        )


# --- Execution ---
search_path = input("Enter the path of the folder to clean: ").strip()

if os.path.isdir(search_path):
    archive_duplicates(search_path)
else:
    print("Invalid folder path.")
