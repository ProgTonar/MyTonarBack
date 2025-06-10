from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Appeal(Base):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
