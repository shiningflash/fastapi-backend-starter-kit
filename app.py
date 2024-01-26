import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_URL = "postgresql://postgres:postgres@db:5432/test_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Dependency to get database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
