from pydantic import BaseModel


class Book(BaseModel):
    name: str
    author: str
    price: int
    description: str

    class Config:
        orm_mode = True


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True
