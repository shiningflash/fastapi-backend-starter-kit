from db import db, metadata, sqlalchemy


books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.JSON),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("description", sqlalchemy.String),
)

authors = sqlalchemy.Table(
    "authors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)


class Book:
    @classmethod
    async def get(cls, id):
        query = books.select().where(books.c.id == id)
        book = await db.fetch_one(query)
        return book

    @classmethod
    async def create(cls, **book):
        query = books.insert().values(**book)
        book_id = await db.execute(query)
        return book_id