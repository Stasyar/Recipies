import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database import engine
from main import app

client = TestClient(app)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="module")
def test_db():
    yield TestingSessionLocal()


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
