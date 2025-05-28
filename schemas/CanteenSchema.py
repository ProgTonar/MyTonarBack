from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Query

class GetReceipt(BaseModel):
    login: str = Field(..., max_length=100)
    date_begin: str = Field(..., max_length=100)
    date_end: str = Field(..., max_length=100)

class GetMenu(BaseModel):
    salads: str # салаты
    soups: str # супы
    mainCourses: str # котлеты разные
    sides: str # гарниры
    drinks: str # напитки
    healthy: str # диетические блюда
    bakery: str # выпечка