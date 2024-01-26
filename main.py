import uvicorn
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from logger import logger
from app.models import User, Blog
from app.schemas import *
from app.db.base import engine, get_db

from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Started!!")
    Base.metadata.create_all(bind=engine)
    logger.info("DB connected!!")
    yield
    logger.info("Shutdown!!")
    logger.info("DB disconnected!!")


app = FastAPI(lifespan=lifespan, debug=True)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


health_router = APIRouter()
book_router = APIRouter()


@health_router.get("/", status_code=200, tags=["health"])
def health_check():
    logger.info(f"Health check route accessed!")
    return {"health_check": "100% OK"}


@book_router.get("/blog/", status_code=200, tags=["blog"])
def get_blogs(db: Session = Depends(get_db)) -> List[BlogList]:
    db_book = db.query(Blog)
    return db_book


# @book_router.post("/blog/", status_code=201, tags=["blog"])
# def create_item(item: BookIn, db: Session = Depends(get_db)) -> BookOut:
#     db_book = Book(**item.model_dump())
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return BookOut(**db_book.__dict__)


# @book_router.get("/books/{id}", status_code=200, tags=["book"])
# def get_book(id: int, db: Session = Depends(get_db)) -> BookOut:
#     db_book = db.query(Book).filter(Book.id == id).first()
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return BookOut(**db_book.__dict__)


# @book_router.put("/books/{id}", status_code=200, tags=["book"])
# def update_item(id: int, book: BookUpdate, db: Session = Depends(get_db)) -> BookOut:
#     db_book = db.query(Book).filter(Book.id == id).first()
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Boook not found")
#     for key, value in book.model_dump().items():
#         setattr(db_book, key, value)
#     db.commit()
#     db.refresh(db_book)
#     return BookOut(**db_book.__dict__)


# @book_router.delete("/books/{id}", status_code=200, tags=["book"])
# def update_item(id: int, book: BookUpdate, db: Session = Depends(get_db)) -> BookOut:
#     db_book = db.query(Book).filter(Book.id == id).first()
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Boook not found")
#     db.delete(db_book)
#     db.commit()
#     return BookOut(**db_book.__dict__)


app.include_router(health_router)
app.include_router(book_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
