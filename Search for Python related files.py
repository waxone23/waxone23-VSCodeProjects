import os


def search_files_for_word(root_path, keyword):
    matches = []
    print(f"Searching for '{keyword}' in {root_path}...\n")

    # os.walk goes through every folder and subfolder
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            # We filter for common text-based extensions to avoid crashing on images/system files
            if file_name.lower().endswith(
                (".txt", ".py", ".md", ".csv", ".log", ".json")
            ):
                full_path = os.path.join(root, file_name)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        # Check if the word is in the file content
                        if keyword.lower() in f.read().lower():
                            matches.append(full_path)
                            print(f"[FOUND] {full_path}")
                except Exception as e:
                    # Skips files that can't be opened (e.g., system-locked files)
                    continue

    return matches


# --- Execution ---
search_dir = input(
    "Enter the directory to search (e.g., C:/Users/YourName/Documents): "
).strip()
word_to_find = input("Enter the word you are looking for: ").strip()

if os.path.isdir(search_dir):
    results = search_files_for_word(search_dir, word_to_find)

    print("\n" + "=" * 30)
    print(f"Search Complete. Found {len(results)} files.")
else:
    print("Invalid directory path.")
