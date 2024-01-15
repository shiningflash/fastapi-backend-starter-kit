from contextlib import asynccontextmanager
from fastapi import FastAPI

from db import db
from logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Started!!")
    await db.connect()
    logger.info("DB connected!!")
    yield
    logger.info("Shutdown!!")
    await db.disconnect()
    logger.info("DB disconnected!!")


app = FastAPI(lifespan=lifespan, debug=True)