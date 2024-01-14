from pydantic import BaseModel


class Author(BaseModel):
    name: str

    class ConfigDict:
        orm_mode = True


class Book(BaseModel):
    name: str
    author: str
    price: int
    description: str

    class ConfigDict:
        orm_mode = True
