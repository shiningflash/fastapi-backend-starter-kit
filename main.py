import uvicorn
import pathlib
from fastapi.middleware.cors import CORSMiddleware
from models import Book as ModelBook
from schema import Book as SchemaBook
from app import app

from fastapi import APIRouter

from logger import logger

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


book_router = APIRouter()
health_router = APIRouter()


@health_router.get("/", status_code=200, tags=["health"])
async def health_check():
    logger.info(f"Health check route accessed!") 
    return {"health_check": "100% OK"}

@book_router.post("/book/", status_code=201, tags=["book"])
async def create_book(book: SchemaBook):
    book_id = await ModelBook.create(**book)
    return {"book_id": book_id}

@book_router.get("/book/{id}", response_model=SchemaBook, status_code=200, tags=["book"])
async def get_book(id: int):
    book = await ModelBook.get(id)
    return SchemaBook(**book)


app.include_router(health_router)
app.include_router(book_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
