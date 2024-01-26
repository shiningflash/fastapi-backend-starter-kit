import os
from databases import Database
from dotenv import load_dotenv
import sqlalchemy

from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from app import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# db = Database(os.environ["DATABASE_URL"])
db = Database("postgresql://postgres:postgres@db:5432/test_db")

metadata = sqlalchemy.MetaData()


# class AppBase(Base):
#     id: Any
#     __name__: str

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()