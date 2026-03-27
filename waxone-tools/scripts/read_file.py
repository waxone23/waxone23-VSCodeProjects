import sys
import glob


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 read_file.py <search_term>", file=sys.stderr)
        return 1

    search_term = sys.argv[1].lower()
    found_any = False

    for filename in glob.glob("*.py"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if search_term in line.lower():
                    print(f"\n--- Found in {filename} ---")
                    # Context: One line before
                    if i > 0:
                        print(f"  {i}: {lines[i-1].strip()}")
                    # The Match (Line i+1 for human counting)
                    print(f"> {i+1}: {line.strip()}")
                    # Context: One line after
                    if i < len(lines) - 1:
                        print(f"  {i+2}: {lines[i+1].strip()}")
                    found_any = True
        except Exception:
            continue

    return 0 if found_any else 1


if __name__ == "__main__":
    sys.exit(main())
