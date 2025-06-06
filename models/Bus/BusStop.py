from sqlalchemy import Column, Integer, String, DateTime, JSON, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class BusStop(Base):
    __tablename__ = "bus_stops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    arrival_time = Column(Time, nullable=False)  
    coordinate = Column(JSON, nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    routes = relationship("BusRoute", secondary="bus_route_stops", back_populates="stops")