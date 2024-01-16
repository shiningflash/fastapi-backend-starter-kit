import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from models import Book
from schema import BookIn, BookOut
from app import engine, get_db

from fastapi import APIRouter

from logger import logger

from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, Session, Mapped
from pydantic import BaseModel

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(BaseModel):
    id: int
    name: str


class ItemCreate(BaseModel):
    name: str


class ItemUpdate(BaseModel):
    name: Optional[str]


class DBItem(Base):
    __tablename__ = "items"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True, index=True, nullable=False)
    

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    db_item = DBItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return Item(**db_item.__dict__)


# book_router = APIRouter()
# health_router = APIRouter()


# @health_router.get("/", status_code=200, tags=["health"])
# async def health_check():
#     logger.info(f"Health check route accessed!") 
#     return {"health_check": "100% OK"}


# @book_router.post("/book/", response_model=BookOut, status_code=201, tags=["book"])
# async def create_book(book: BookIn):
#     book_id = await Book.create(**book.__dict__)
#     book = await Book.get(book_id)
#     return BookOut(**book)


# @book_router.get("/book/{id}", response_model=BookOut, status_code=200, tags=["book"])
# async def get_book(id: int):
#     book = await Book.get(id)
#     return BookOut(**book)


# app.include_router(health_router)
# app.include_router(book_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
