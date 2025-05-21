from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://admin:test1234@localhost:3306/pyapi'

## для sqlLite
## engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) 

## для mySql
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
