"""Requests-based examples for testing the Library API.

Run this after starting the FastAPI app, for example:
uvicorn library:app --reload
"""

# CELL 1 -- FETCH ALL BOOKS
import requests

response = requests.get("http://localhost:8000/books")

print(response.status_code)  # 200
print(response.ok)  # True
print(response.json())  # [] -- empty list for now


# CELL 2 -- POST A NEW BOOK
response = requests.post(
    "http://localhost:8000/books",
    json={
        "title": "Clean Code",
        "author": "Robert Martin",
        "year": 2008,
    },
)

print(response.status_code)  # 201
print(response.json())  # {'id': 1, 'title': 'Clean Code', ...}

# Now fetch all books again -- we should see one book
all_books = requests.get("http://localhost:8000/books")
print(all_books.json())


# CELL 3 -- GET ONE BOOK AND HANDLE 404
# Fetch a book that exists
r = requests.get("http://localhost:8000/books/1")
print(r.status_code)  # 200
print(r.json())  # {'id': 1, 'title': 'Clean Code', ...}

# Fetch a book that does NOT exist
r2 = requests.get("http://localhost:8000/books/999")
print(r2.status_code)  # 404
print(r2.ok)  # False
print(r2.json())  # {'detail': 'Book 999 not found'}


# CELL 4 -- RAISE_FOR_STATUS() + CONNECTIONERROR
import sys


def fetch_book(book_id: int):
    try:
        r = requests.get(f"http://localhost:8000/books/{book_id}")
        r.raise_for_status()  # raises if 4xx or 5xx
        return r.json()
    except requests.exceptions.ConnectionError:
        print("Server is not running", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}", file=sys.stderr)
        return None


book = fetch_book(1)
print(book)

missing = fetch_book(999)
print(missing)  # None -- error was printed to stderr
