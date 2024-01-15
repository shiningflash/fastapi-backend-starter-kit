from pydantic import BaseModel


class AuthorIn(BaseModel):
    name: str

    class ConfigDict:
        orm_mode = True


class AuthorOut(AuthorIn):
    id: int

    class ConfigDict:
        orm_mode = True


class BookIn(BaseModel):
    name: str
    author: str
    price: int
    description: str

    class ConfigDict:
        orm_mode = True


class BookOut(BookIn):
    id: int

    class ConfigDict:
        orm_mode = True
