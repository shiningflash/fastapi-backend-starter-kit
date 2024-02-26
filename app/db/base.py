from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():  # Dependency to get database session
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
