from pydantic import BaseModel


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Book(BaseModel):
    name: str
    author: Author
    price: int
    description: str

    class Config:
        orm_mode = True
