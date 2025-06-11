from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class LikeAppeal(Base):
    __tablename__ = 'like_appeals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    appeal_id = Column(Integer, ForeignKey('appeals.id', ondelete='CASCADE'), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    appeal = relationship('Appeal', back_populates='likes')
