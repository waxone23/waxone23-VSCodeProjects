import sys
import requests


def main():
    url = "http://localhost:8000/books"
    books_to_add = [
        {"title": "The Hobbit", "author": "Tolkien", "year": 1937},
        {"title": "1984", "author": "Orwell", "year": 1949},
        {"title": "Python 101", "author": "Guido", "year": 2024},
    ]

    try:
        for idx, book in enumerate(books_to_add, start=1):
            response = requests.post(url, json=book, timeout=5)
            if response.status_code != 201:
                print(
                    f"Error: Book {idx} was not created. "
                    f"Status={response.status_code}, body={response.text}",
                    file=sys.stderr,
                )
                return 1
        print("Success: all 3 books were created.")
        return 0
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to FastAPI server.", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"Error: Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
