from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Query

class GetReceipt(BaseModel):
    login: str = Field(..., max_length=100)
    date_begin: str = Field(..., max_length=100)
    date_end: str = Field(..., max_length=100)

class CreateMenu(BaseModel):
    name: str = Field(..., max_length=100)
    code: int
    cost: int
    weight: str = Field(..., max_length=100)
    category: str = Field(..., max_length=100)
    date: str = Field(..., max_length=100)

class CreateScore(BaseModel):
    user_id: int
    food_id: int
    score: int