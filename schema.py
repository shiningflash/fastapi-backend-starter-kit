from pydantic import BaseModel


class Author(BaseModel):
    name: str
    country: str

    class Config:
        orm_mode = True


class Book(BaseModel):
    name: str
    author: str
    price: int
    description: str

    class Config:
        orm_mode = True
