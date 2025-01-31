from sqlalchemy import Column, Integer, String

from app.database import Base


class Recipy(Base):
    __tablename__ = "Recipy"
    recipy_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cooking_time = Column(Integer, index=True)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
    views = Column(Integer, default=0)
