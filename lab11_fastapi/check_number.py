import sys


def main():
    # a) If no argument is given
    if len(sys.argv) < 2:
        print("Usage: python check_number.py <number>", file=sys.stderr)
        return 2

    val_str = sys.argv[1]

    # b) If the argument is not a valid integer
    try:
        number = int(val_str)
    except ValueError:
        print(f"Error: '{val_str}' is not a valid integer.", file=sys.stderr)
        return 1

    # c) If the number is negative
    if number < 0:
        print(
            f"Error: {number} is negative. Please use a positive number.",
            file=sys.stderr,
        )
        return 1

    # d) If everything is fine
    print(f"Valid number: {number}")
    return 0


if __name__ == "__main__":
    # This captures the return value of main and sends it to the OS
    sys.exit(main())
