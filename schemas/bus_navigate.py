from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.schemas.stop import Stop, StopInRoute
from app.schemas.common import Coordinates

class BusNavigateBase(BaseModel):
    title: str
    name_start: str
    name_end: str
    dots_start: Coordinates
    dots_end: Coordinates

    model_config = ConfigDict(from_attributes=True)

class BusNavigateCreate(BusNavigateBase):
    stops: Optional[List[StopInRoute]] = []

class BusNavigateUpdate(BaseModel):
    title: Optional[str] = None
    name_start: Optional[str] = None
    name_end: Optional[str] = None
    dots_start: Optional[Coordinates] = None
    dots_end: Optional[Coordinates] = None
    stops: Optional[List[StopInRoute]] = None

    model_config = ConfigDict(from_attributes=True)

class BusNavigate(BusNavigateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    stops: List[Stop] = []