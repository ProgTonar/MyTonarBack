from database import SessionLocal, engine
from models.Appeal.StatusAppealModel import StatusAppeal
from database.factories.CreateStatusAppealsFactory import CreateStatusAppeals

def CreateStatusAppealsScript():
    db = SessionLocal()
    try:
        existing = db.query(StatusAppeal).count()

        if existing > 0:
            print('Стартовые данные уже существуют')
            return

        CreateStatusAppeals.create_batch(4)

        print('Данные загружены успешно')
    except Exception as e:
        print(f"Произошла ошибка в загрузке данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    CreateStatusAppealsScript()
