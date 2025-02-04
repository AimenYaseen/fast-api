import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Tomato"}


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
