import models
import schemas
from database import async_session, engine
from fastapi import FastAPI, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.future import select

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    async with async_session() as session:
        await session.close()
        await engine.dispose()


@app.get(
    "/all_recipies/",
    status_code=200,
    response_model=list[schemas.FirstWindow],
    summary="Все рецепты",
    description="Этот эндпоинт возвращает список всех рецептов в базе данных",
)
async def all_recipies() -> list[schemas.FirstWindow]:
    async with async_session() as session:
        res = select(models.Recipy).order_by(
            desc(models.Recipy.views), asc(models.Recipy.cooking_time)
        )
        result = await session.execute(res)
        recipies = result.scalars().all()
        print(f"'/all_recipies': {recipies}")
        return [schemas.FirstWindow.from_orm(recipy) for recipy in recipies]


@app.get(
    "/recipy/{recipy_id}",
    status_code=200,
    response_model=schemas.SecondWindow,
    summary="Рецепт по id",
    description="""Этот эндпоинт возвращает информацию
    для одного рецепта по его id""",
)
async def recipy_by_id(recipy_id: int) -> schemas.SecondWindow:
    async with async_session() as session:
        res = select(models.Recipy).filter(models.Recipy.recipy_id == recipy_id)
        result = await session.execute(res)
        recipy = result.scalar_one_or_none()

        if recipy is None:
            raise HTTPException(status_code=404, detail="Recipy not found")

        recipy.views += 1
        await session.commit()

        return schemas.SecondWindow.from_orm(recipy)


@app.post(
    "/add_recipy/",
    status_code=201,
    response_model=schemas.RecipyIn,
    summary="Добавить новый рецепт",
    description="Этот эндпоинт добавляет новый рецепт в базу данных",
)
async def create_recipy(recipy: schemas.RecipyIn) -> schemas.RecipyIn:
    async with async_session() as session:
        new_recipy = models.Recipy(
            name=recipy.name,
            cooking_time=recipy.cooking_time,
            ingredients=recipy.ingredients,
            description=recipy.description,
        )

        session.add(new_recipy)
        await session.commit()
        await session.refresh(new_recipy)

        return schemas.RecipyIn.from_orm(new_recipy)
