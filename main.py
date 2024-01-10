import uvicorn
from models import Book as ModelBook
from schema import Book as SchemaBook
from app import app
from db import db


@app.post("/book/")
async def create_book(book: SchemaBook):
    book_id = await ModelBook.create(**book.dict())
    return {"book_id": book_id}


@app.get("/book/{id}", response_model=SchemaBook)
async def get_book(id: int):
    book = await ModelBook.get(id)
    return SchemaBook(**book).dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)