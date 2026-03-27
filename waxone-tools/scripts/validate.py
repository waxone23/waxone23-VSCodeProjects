import sys
import os


def main() -> int:
    path = "data/data.csv"

    # 1. Check if it exists
    if not os.path.exists(path):
        print(f"❌ Error: {path} not found", file=sys.stderr)
        return 1

    # 2. Check if it has actual data (Size > 0 bytes)
    if os.path.getsize(path) == 0:
        print(f"⚠️ Error: {path} is EMPTY! Nothing to process.", file=sys.stderr)
        return 1

    print(f"✅ {path} contains data and is ready!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
