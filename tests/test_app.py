import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base
from app.main import create_app


@pytest_asyncio.fixture
async def app_instance():
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    app = create_app(async_session, engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield app

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(app_instance):
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app_instance)
    ) as c:
        yield c


@pytest.mark.asyncio
async def test_all_recipies(client):

    recipy_data = {
        "name": "Паста с соусом",
        "cooking_time": 30,
        "ingredients": "pastaa",
        "description": "good",
        "views": 0,
    }

    response = await client.post("/add_recipy/", json=recipy_data)
    assert response.status_code == 201

    response = await client.get("/all_recipies/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
