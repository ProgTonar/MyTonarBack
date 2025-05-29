from database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.Canteen.Food import Food

class FoodFeedback(Base):
    __tablename__ = 'food_feedbacks'

    id = Column(Integer, primary_key=True, index=True)
    feedback = Column(String(255), nullable=False)
    food_id = Column(Integer, ForeignKey('foods.id'), index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    food = relationship('Food', back_populates='feedback')

