from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Appeal(Base):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    answer = Column(String(255), nullable=True)
    status_id = Column(Integer, ForeignKey('status_appeals.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    status = relationship('StatusAppeal', back_populates="appeals")
    likes = relationship('LikeAppeal', back_populates='appeal')
