from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    age: int
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
