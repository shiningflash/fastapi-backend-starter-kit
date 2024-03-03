import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.logger import logger
from app.db.base import engine

from app.db.base_class import Base
from app.routes import router as api_router


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


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
