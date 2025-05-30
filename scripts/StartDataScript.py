from database import SessionLocal, engine
from models import FoodCategory
from database.factories.StartDataFactory import StartDataFactory

def load_initial_data():
    db = SessionLocal()
    try:
        existing = db.query(FoodCategory).count()

        if existing > 0:
            print('Стартовые данные уже существуют')
            return

        StartDataFactory.create_batch(7)

        print('Данные загружены успешно')
    except Exception as e:
        print(f"Произошла ошибка в загрузке данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    load_initial_data()
