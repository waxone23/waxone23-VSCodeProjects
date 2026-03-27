from pydantic import BaseModel, ValidationError
from typing import Optional


class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True
    isbn: Optional[str] = None


b1 = Book(title="Clean Code", author="Robert Martin", year=2008)
b2 = Book(title="1984", author="George Orwell", year=1949, available=False)
print(b1)
print(b2)

try:
    Book(title="X", author="Y", year="nineteen-eighty-four")
except ValidationError as err:
    print(err.errors()[0]["msg"])

try:
    Book(author="Y", year=2020)
except ValidationError as err:
    print(err.errors()[0]["msg"])

print(b1.model_dump())

b3 = Book(
    title="Python Tricks", author="Dan Bader", year=2017, isbn="978-1-7750-4294-5"
)
b4 = Book(title="Fluent Python", author="Luciano Ramalho", year=2022)
print(b3.isbn)
print(b4.isbn)
