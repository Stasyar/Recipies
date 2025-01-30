import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from main import app
from database import engine

client = TestClient(app)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
