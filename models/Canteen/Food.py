from database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Food(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('food_categories.id'), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    category = relationship("FoodCategory", back_populates="foods")
    feedback = relationship('FoodFeedback', back_populates='food')
    score = relationship('FoodScore', back_populates='food')