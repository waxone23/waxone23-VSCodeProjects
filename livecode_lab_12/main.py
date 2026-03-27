from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    year: int


# Explicit typing for mypy
db: dict[int, Book] = {}


@app.post("/books", status_code=201)
async def create_book(book: Book) -> Book:
    book_id = len(db) + 1
    db[book_id] = book
    return book


@app.get("/books")
async def list_books() -> list[Book]:
    return list(db.values())


@app.get("/books/{book_id}")
async def get_book(book_id: int) -> Book:
    if book_id not in db:
        raise HTTPException(status_code=404, detail="Book not found")
    return db[book_id]


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    if book_id not in db:
        raise HTTPException(status_code=404, detail="Book not found")
    del db[book_id]
    return {"message": "Book deleted"}
