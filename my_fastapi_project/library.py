from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI()

# --- STEP 9: DATABASE PERSISTENCE LOGIC ---
DATABASE_FILE = "library_data.json"


def save_db():
    # JSON requires string keys, so we convert the integer IDs to strings
    with open(DATABASE_FILE, "w") as f:
        json.dump({str(k): v.model_dump() for k, v in db.items()}, f, indent=4)


def load_db():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            data = json.load(f)
            # Convert string keys back to integers and data back to BookCreate objects
            return {int(k): BookCreate(**v) for k, v in data.items()}
    return {}


# --- STEP 2 & 3: MODELS ---
class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True


class BookResponse(BookCreate):
    id: int


# --- INITIALIZE DATABASE ---
# This runs once when the server starts
db = load_db()

# --- ROUTES ---


@app.get("/")
def root():
    return {"message": "Welcome to the Library API!"}


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate):
    # Find the highest ID and add 1, or start at 1 if empty
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = book
    save_db()  # Save to file!
    return {"id": new_id, **book.model_dump()}


@app.get("/books", response_model=List[BookResponse])
def list_books():
    return [{"id": bid, **book.model_dump()} for bid, book in db.items()]


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    if book_id not in db:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return {"id": book_id, **db[book_id].model_dump()}


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in db:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    del db[book_id]
    save_db()  # Save to file!
    return None


@app.get("/search")
def search_books(title: str):
    results = []
    for book_id, book in db.items():
        if title.lower() in book.title.lower():
            results.append({"id": book_id, **book.model_dump()})
    return results
