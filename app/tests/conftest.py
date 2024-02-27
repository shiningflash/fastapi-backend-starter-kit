import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base
from app.db.base import get_db
from core.config import settings
from main import app
from app.tests.utils.utils import push_data_into_test_db

from core.logger import logger


engine = create_engine(settings.TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base.metadata.create_all(bind=engine, checkfirst=True)

db = TestingSessionLocal()


@pytest.fixture
def my_test_db():
    yield TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(table.delete())
                trans.commit()
            except:
                trans.rollback()
                raise


@pytest.fixture()
def client(my_test_db):
    def test_my_test_db():
        return my_test_db
    
    app.dependency_overrides[get_db] = test_my_test_db
    
    with TestClient(app) as test_client:
        push_data_into_test_db(my_test_db)
        yield test_client
    app.dependency_overrides.clear()
