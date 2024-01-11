from typing import AsyncIterator

import os
import httpx
import pytest
import pytest_asyncio

from app import app


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url=os.environ["BASE_URL"]) as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(client: httpx.AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "100% OK"}
