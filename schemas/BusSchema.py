from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from schemas.CommonSchemaa import Coordinates

# class BusNavigateBase(BaseModel):
#     title: str
#     name_start: str
#     name_end: str
#     dots_start: Coordinates
#     dots_end: Coordinates

#     model_config = ConfigDict(from_attributes=True)

# class BusNavigateCreate(BusNavigateBase):
#     stops: int

# class BusNavigateUpdate(BaseModel):
#     title: Optional[str] = None
#     name_start: Optional[str] = None
#     name_end: Optional[str] = None
#     dots_start: Optional[Coordinates] = None
#     dots_end: Optional[Coordinates] = None
#     stops: int

#     model_config = ConfigDict(from_attributes=True)

# class BusNavigate(BusNavigateBase):
#     id: int
#     created_at: datetime
#     updated_at: Optional[datetime]
#     stops: int

# class StopBase(BaseModel):
#     name: str
#     arrival_time: str
#     coordinate: Coordinates

#     model_config = ConfigDict(from_attributes=True)

# class StopUpdate(BaseModel):
#     name: Optional[str] = None
#     arrival_time: Optional[str] = None
#     coordinate: Optional[Coordinates] = None

#     model_config = ConfigDict(from_attributes=True)

# class Stop(StopBase):
#     id: int
#     created_at: datetime
#     updated_at: Optional[datetime]

# class StopInRoute(StopBase):
#     id: Optional[int] = None
#     should_delete: Optional[bool] = False