from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from contextlib import asynccontextmanager
from redis.asyncio import Redis
import app.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация Redis
    redis_client = Redis(
        host='localhost', 
        port=6379,
        password='test1234',
        decode_responses=True
    )
    
    try:
        await redis_client.ping()
        app.state.redis = redis_client
        print("✅ Redis подключён успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        raise
    
    print("Запуск приложения...")
    
    try:
        yield  
    finally:
        # Завершение работы
        print("Закрытие соединения с Redis...")
        await redis_client.close()
        print("Завершение приложения...")
    
app = FastAPI(
    title="Бэк Мой Тонар",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:9091",
        "http://localhost:5173",
        "http://127.0.0.1:5173", 
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-Requested-With", "Authorization"]
)

app.include_router(api_router, prefix="/api")

@app.get(
    "/", 
    tags=["Главная"],
    summary="Корневой эндпоинт",
    description="Возвращает приветственное сообщение"
)
async def read_root():
    return {"message": "Добро пожаловать в сервис Мой Тонар"}