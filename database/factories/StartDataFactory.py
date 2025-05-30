import factory
from factory.alchemy import SQLAlchemyModelFactory
from models import FoodCategory
from database import SessionLocal

class StartDataFactory(SQLAlchemyModelFactory):
    class Meta:
        model = FoodCategory
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"
    
    name = factory.Iterator([
        'salads', 
        'soups', 
        'mainCourses', 
        'sides', 
        'drinks', 
        'healthy', 
        'bakery'
    ])