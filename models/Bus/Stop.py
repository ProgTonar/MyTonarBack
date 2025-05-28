from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base
from models.Bus.Bus import bus_route_stops

class Stop(Base):
    __tablename__ = "bus_stops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    arrival_time = Column(String(50), nullable=False)  
    coordinate = Column(JSON, nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    bus_navigates = relationship("route", secondary=bus_route_stops, back_populates="bus_stops") 