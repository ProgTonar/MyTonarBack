from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Contacts(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    v_phonenumber = Column(String(255), nullable=True)
    short_phonenumber = Column(String(255), nullable=True)
    mobile_phone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    
    def __repr__(self):
        return f"<Contacts {self.name}>"