import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager
from fastapi import FastAPI

from db import db, metadata
from logger import logger


DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Started!!")
    await db.connect()
    metadata.create_all(bind=engine)
    logger.info("DB connected!!")
    yield
    logger.info("Shutdown!!")
    await db.disconnect()
    logger.info("DB disconnected!!")


app = FastAPI(lifespan=lifespan, debug=True)


# Dependency to get database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
