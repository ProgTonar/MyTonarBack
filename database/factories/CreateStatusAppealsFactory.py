import factory
from factory.alchemy import SQLAlchemyModelFactory
from models.Appeal import StatusAppeal
from database import SessionLocal

class CreateStatusAppeals(SQLAlchemyModelFactory):
    class Meta:
        model = StatusAppeal
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Iterator([ # колонка в таблице
        'На рассмотрении', # данные для колонки
        'В работе',
        'Отказано',
        'Решено',
    ])