from typing import AsyncIterator
import httpx, os
import pytest
import pytest_asyncio

from main import app

@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url=os.environ["BASE_URL"]) as client:
        yield client

@pytest.mark.asyncio
async def test_health_check(client: httpx.AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "100% OK"}

@pytest.mark.asyncio
async def test_create_book(client: httpx.AsyncClient) -> None:
    payload = {
        "name": "Eat that frog",
        "author": "Brian Tracy",
        "price": 280,
        "description": "Book for procastination."
    }
    response = await client.post("/book/", json=payload)
    assert response.status_code == 201
    
@pytest.mark.asyncio
async def test_get_book(client: httpx.AsyncClient) -> None:
    response = await client.get("/book/2")
    assert response.status_code == 200