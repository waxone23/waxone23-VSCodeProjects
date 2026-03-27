#!/bin/bash
echo "--- Installerer verktoy ---"
pip install fastapi uvicorn pydantic pytest ruff pre-commit httpx

echo "--- Oppretter main.py ---"
cat <<INNEREOF > main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year: int

books = {}

@app.post("/books", status_code=201)
async def create_book(book: Book):
    books[1] = book
    return book

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
INNEREOF

echo "--- Oppretter test_books_api.py ---"
cat <<INNEREOF > test_books_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    r = client.post('/books', json={
        'title': 'Clean Code',
        'author': 'Robert Martin',
        'year': 2008
    })
    assert r.status_code == 201
    assert r.json()['title'] == 'Clean Code'

def test_get_missing_book():
    r = client.get('/books/9999')
    assert r.status_code == 404
INNEREOF

echo "--- Konfigurerer Pre-commit ---"
cat <<INNEREOF > .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
      - id: ruff-format
INNEREOF

git init
pre-commit install

echo "--- Oppretter GitHub Actions CI ---"
mkdir -p .github/workflows
cat <<INNEREOF > .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.12'}
      - run: pip install fastapi uvicorn pydantic pytest ruff httpx
      - run: ruff check .
      - run: pytest
INNEREOF

echo "--- Ferdig ---"
