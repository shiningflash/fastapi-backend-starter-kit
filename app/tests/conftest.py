import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base, get_db
from core.config import settings
from main import app


engine = create_engine(settings.DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine, checkfirst=True)


@pytest.fixture
def db():
    print('\n\n\n\n >>>> \n\n\n\n')
    yield TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        with engine.connect() as conn:
            conn.execute(table.delete())
            conn.commit()


@pytest.fixture
def client(db):
    print('\n\n\n\n >>>> \n\n\n\n')
    def test_db():
        return db

    app.dependency_overrides[get_db] = test_db
    return TestClient(app)
