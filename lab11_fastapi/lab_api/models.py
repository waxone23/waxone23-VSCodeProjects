from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: bool = True
