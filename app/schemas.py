from pydantic import BaseModel, Field


class BaseRecipy(BaseModel):
    name: str = Field(..., description="Название рецепта")
    cooking_time: int = Field(..., description="Время приготовления")


class FirstWindow(BaseRecipy):
    views: int = 0

    class Config:
        from_attributes = True


class SecondWindow(BaseRecipy):
    recipy_id: int = Field(..., description="id рецепта")
    ingredients: str = Field(..., description="Ингридиенты рецепта")
    description: str = Field(..., description="Описание рецепта")

    class Config:
        from_attributes = True


class RecipyIn(BaseRecipy):
    ingredients: str = Field(..., description="Ингридиенты рецепта")
    description: str = Field(..., description="Описание рецепта")

    class Config:
        from_attributes = True
