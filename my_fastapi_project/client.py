import os
import sys
import requests

DEFAULT_BASE_URLS = ["http://localhost:8001", "http://localhost:8000"]


def resolve_books_url() -> str:
    env_base_url = os.getenv("BOOKS_API_URL")
    candidates = [env_base_url] if env_base_url else DEFAULT_BASE_URLS

    for base_url in candidates:
        books_url = f"{base_url}/books"
        try:
            response = requests.get(books_url, timeout=2)
            if response.status_code == 200:
                return books_url
        except requests.exceptions.ConnectionError:
            continue

    if env_base_url:
        raise requests.exceptions.ConnectionError(
            f"No reachable books API at {env_base_url}."
        )

    raise requests.exceptions.ConnectionError(
        "Could not find a books API on localhost:8001 or localhost:8000."
    )


def add_books(books_url: str, books: list[dict]) -> list[dict]:
    existing_response = requests.get(books_url, timeout=10)
    existing_response.raise_for_status()
    existing_books = existing_response.json()
    existing_keys = {
        (b.get("title"), b.get("author"), b.get("year")) for b in existing_books
    }

    created = []
    for book in books:
        key = (book.get("title"), book.get("author"), book.get("year"))
        if key in existing_keys:
            continue

        response = requests.post(books_url, json=book, timeout=10)
        if response.status_code == 201:
            created_book = response.json()
            created.append(created_book)
            existing_keys.add(
                (
                    created_book.get("title"),
                    created_book.get("author"),
                    created_book.get("year"),
                )
            )
        else:
            print(
                f"Failed to add '{book.get('title', 'unknown')}': "
                f"{response.status_code} {response.text}",
                file=sys.stderr,
            )
    return created


def print_all_books(books_url: str) -> list[dict]:
    response = requests.get(books_url, timeout=10)
    response.raise_for_status()
    books = response.json()

    print("All books:")
    for book in books:
        print(f"{book['title']} - {book['author']}")
    return books


def fetch_book(books_url: str, book_id: int) -> dict | None:
    response = requests.get(f"{books_url}/{book_id}", timeout=10)
    if response.status_code == 404:
        detail = response.json().get("detail", "Not found")
        print(f"Book {book_id}: {detail}", file=sys.stderr)
        return None
    response.raise_for_status()
    return response.json()


def main() -> int:
    books_to_add = [
        {
            "title": "Clean Code",
            "author": "Robert Martin",
            "year": 2008,
            "available": True,
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt, David Thomas",
            "year": 1999,
            "available": True,
        },
        {
            "title": "Domain-Driven Design",
            "author": "Eric Evans",
            "year": 2003,
            "available": False,
        },
        {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "year": 1999,
            "available": True,
        },
        {
            "title": "Design Patterns",
            "author": "Erich Gamma et al.",
            "year": 1994,
            "available": False,
        },
    ]

    try:
        books_url = resolve_books_url()
        print(f"Using API endpoint: {books_url}")

        # Adds 5 books (covers "at least three" and bonus loop requirement).
        created_books = add_books(books_url, books_to_add)
        print(f"Created {len(created_books)} book(s).")

        all_books = print_all_books(books_url)

        if all_books:
            first_id = all_books[0]["id"]
            one_book = fetch_book(books_url, first_id)
            if one_book:
                print("\nOne specific book:")
                print(one_book)
        else:
            print("No books available to fetch by ID.")

        print("\nTry missing book ID 999:")
        missing = fetch_book(books_url, 999)
        if missing is None:
            print("Handled missing book gracefully.")

        print("\nAvailable books only:")
        seen_available = set()
        for book in all_books:
            unique_key = (book.get("title"), book.get("author"), book.get("year"))
            if book.get("available") is True and unique_key not in seen_available:
                print(f"{book['title']} - {book['author']}")
                seen_available.add(unique_key)

        return 0
    except requests.exceptions.ConnectionError:
        print(
            "Could not connect to the API server. "
            "Make sure it is running (for this project use: uvicorn library:app --reload --port 8001). "
            "You can also set BOOKS_API_URL, for example: BOOKS_API_URL=http://localhost:8001",
            file=sys.stderr,
        )
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
