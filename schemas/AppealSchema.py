from pydantic import BaseModel, Field
from typing import Optional

class CreateAppeal(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=1000)
    status_id: int
    user_id: int

class AddAnswer(BaseModel):
    id: int
    answer: str = Field(..., min_length=1, max_length=255)

class ChangeActive(BaseModel):
    id: int
    active: bool

class PutLike(BaseModel):
    user_id: int
    appeal_id: int