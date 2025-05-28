from sqlalchemy import Column, Integer, String, DateTime, JSON, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

bus_route_stops = Table(
    'bus_route_stops',
    Base.metadata,
    Column('bus_navigate_id', Integer, ForeignKey('bus_routes.id'), primary_key=True),
    Column('stop_id', Integer, ForeignKey('bus_stops.id'), primary_key=True)
)

class BusNavigate(Base):
    __tablename__ = "bus_routes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    name_start = Column(String(255), nullable=False)
    name_end = Column(String(255), nullable=False)
    dots_start = Column(JSON, nullable=False)  
    dots_end = Column(JSON, nullable=False)    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    stops = relationship("stop", secondary=bus_route_stops, back_populates="bus_routes") 


    