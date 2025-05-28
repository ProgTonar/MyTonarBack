from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.MoneyRoute import router as MoneyRoute
from routes.CanteenRoute import router as CanteenRoute
from database import Base, engine

    
app = FastAPI(
    title="МОЙ ТОНАР API",
    version="1.0.0",
    redoc_url=None
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(BusRoute, prefix="/bus", tags=["Расписание автобусов"])
# app.include_router(ContactsRoute, prefix="/contact", tags=["Контакты"])
app.include_router(MoneyRoute, prefix="/api/money", tags=["Расчетный листок"])
app.include_router(CanteenRoute, prefix="/api/canteen", tags=["Столовая"])

@app.get("/")
async def root():
    return {"message": "Hello World!"}