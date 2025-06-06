from pydantic import BaseModel, Field
from typing import Optional
from datetime import time

class Coordinate(BaseModel):
    x: float
    y: float

class CoordinteUpdate(BaseModel):
    x: Optional[float] = Field(None)
    y: Optional[float] = Field(None)
    
class BusRouteSchema(BaseModel):
    title: str
    name_start: str
    name_end: str
    dots_start: Coordinate
    dots_end: Coordinate

class BusRouteUpdateSchema(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=255)
    name_start: str = Field(..., min_length=1, max_length=255)
    name_end: str = Field(..., min_length=1, max_length=255)
    dots_start: CoordinteUpdate
    dots_end: CoordinteUpdate
    
class StopCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    time: time
    coordinate: Coordinate

class StopUpdateSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=255)
    time: time
    coordinate: Coordinate

class AddStopToRoute(BaseModel):
    stop_id: int
    route_id: int
