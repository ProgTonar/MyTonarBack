from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.common import Coordinates

class StopBase(BaseModel):
    name: str
    arrival_time: str
    coordinate: Coordinates

    model_config = ConfigDict(from_attributes=True)

class StopCreate(StopBase):
    pass

class StopUpdate(BaseModel):
    name: Optional[str] = None
    arrival_time: Optional[str] = None
    coordinate: Optional[Coordinates] = None

    model_config = ConfigDict(from_attributes=True)

class Stop(StopBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class StopInRoute(StopBase):
    id: Optional[int] = None
    should_delete: Optional[bool] = False