from contextlib import asynccontextmanager
from fastapi import FastAPI

from db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Started!!")
    await db.connect()
    yield
    print("Shutdown!!")
    await db.disconnect()


app = FastAPI(lifespan=lifespan, debug=True)