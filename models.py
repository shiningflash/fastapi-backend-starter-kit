from sqlalchemy import create_engine, String, Integer, Column

from app import Base


class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True, index=True, nullable=False)
    author = Column(String(25))
    price = Column(Integer())
    description = Column(String(100))


class Author(Base):
    __tablename__ = "authors"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
