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
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    name_start: Optional[str] = Field(None, min_length=1, max_length=255)
    name_end: Optional[str] = Field(None, min_length=1, max_length=255)
    dots_start: Optional[CoordinteUpdate] = Field(None)
    dots_end: Optional[CoordinteUpdate] = Field(None)
    
class StopCreateSchema(BaseModel):
    name: str
    time: time
    coordinate: Coordinate
