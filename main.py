import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter

from core.logger import logger
from app.schemas import *
from app.db.base import engine

from app.models import Base
from app.api.user import user_router


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


@health_router.get("/", status_code=200, tags=["health"])
def health_check():
    logger.info(f"Health check route accessed!")
    return {"health_check": "100% OK"}


app.include_router(health_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
