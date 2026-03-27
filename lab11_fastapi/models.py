from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True


class BookResponse(BookCreate):
    id: int
