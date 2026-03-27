from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from models import BookCreate, BookResponse

app = FastAPI()

# In-memory store for this lab.
books_db: dict[int, BookResponse] = {}
id_counter = 1


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate) -> BookResponse:
    global id_counter
    new_book = BookResponse(id=id_counter, **book.model_dump())
    books_db[id_counter] = new_book
    id_counter += 1
    return new_book


@app.get("/books", response_model=list[BookResponse])
def get_all_books() -> list[BookResponse]:
    return list(books_db.values())


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int) -> BookResponse:
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int) -> Response:
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return Response(status_code=204)
