import sys
import os


def main():
    if len(sys.argv) < 2:
        filename = input("Enter filename: ").strip()
        if not filename:
            print("Error: No filename provided.", file=sys.stderr)
            sys.exit(2)
    else:
        filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(filename, "r") as f:
        print(f.read())
        sys.exit(0)


if __name__ == "__main__":
    main()
