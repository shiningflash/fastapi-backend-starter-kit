import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base
from app.db.base import get_db
from core.config import settings
from main import app


engine = create_engine(settings.DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base.metadata.create_all(bind=engine, checkfirst=True)


# @pytest.fixture
# def db():
#     yield TestingSessionLocal()
#     for table in reversed(Base.metadata.sorted_tables):
#         with engine.connect() as conn:
#             conn.execute(table.delete())
#             conn.commit()


# @pytest.fixture
# def client(db):
#     def test_db():
#         return db

#     app.dependency_overrides[get_db] = test_db
#     return TestClient(app)


db = TestingSessionLocal()


@pytest.fixture
def test_db():
    yield db
    db.close()


@pytest.fixture()
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def override_get_db(test_db):
    def override():
        return test_db
    return override
