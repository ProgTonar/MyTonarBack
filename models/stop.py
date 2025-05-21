from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base
from app.models.bus_navigate import stops_has_busnavigate

class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    arrival_time = Column(String(50), nullable=False)  
    coordinate = Column(JSON, nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    bus_navigates = relationship("BusNavigate", secondary=stops_has_busnavigate, back_populates="stops") 