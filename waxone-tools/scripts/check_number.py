import sys


def main() -> int:
    # 1. Check for missing argument
    if len(sys.argv) < 2:
        print("Usage: python3 check_number.py <number>", file=sys.stderr)
        return 2

    raw_val = sys.argv[1]

    # 2. Check for integer conversion
    try:
        n = int(raw_val)
    except ValueError:
        print(f"Error: '{raw_val}' is not a valid integer", file=sys.stderr)
        return 1

    # 3. Check for negative
    if n < 0:
        print(f"Error: {n} is negative", file=sys.stderr)
        return 1

    # 4. All good
    print(f"Valid number: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
