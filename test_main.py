import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from main import app
from db import metadata
from schema import BookIn
from app import get_db


DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# def test_health_check():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"health_check": "100% OK"}


# def test_create_book():
#     payload = {
#         "name": "Eat that frog",
#         "author": "Brian Tracy",
#         "price": 280,
#         "description": "Book for procastination."
#     }
#     response = client.post("/book/", json=payload)
#     assert response.status_code == 201


def test_create_item():
    response = client.post(
        "/items/", json={"name": "Test Item 6"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Item 6"
    assert "id" in data


def setup() -> None:
    # create the tables in the test database
    # metadata.create_all(bind=engine)
    
    # create test items here
    # session = TestingSessionLocal()
    # items = BookIn(name="Book 2", author="author here")
    # session.add(item)
    # session.commit()
    # session.close()
    pass


def teardown() -> None:
    # Drop the tables in the test database 
    # CAUTION: if test database if different
    # metadata.drop_all(bind=engine)
    pass