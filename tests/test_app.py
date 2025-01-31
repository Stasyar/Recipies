import pytest
from fastapi.testclient import TestClient

from app.database import async_session
from app.main import app
client = TestClient(app)

TestingSessionLocal = async_session


@pytest.fixture(scope="module")
async def test_db():
    async with TestingSessionLocal() as session:
        yield session


def test_all_recipies(test_db):

    recipy_data = {
        "name": "Паста с соусом",
        "cooking_time": 30,
        "ingredients": "pastaa",
        "description": "good",
        "views": 0,
    }

    response = client.post("/add_recipy/", json=recipy_data)
    assert response.status_code == 201

    response = client.get("/all_recipies/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
