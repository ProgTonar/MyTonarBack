from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import BusRoute, ContactsRoute, MoneyRoute

    
app = FastAPI(
    title="МОЙ ТОНАР API",
    version="1.0.0",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(BusRoute, prefix="/bus", tags=["Расписание автобусов"])
app.include_router(ContactsRoute, prefix="/contact", tags=["Контакты"])
app.include_router(MoneyRoute, prefix="/money", tags=["Расчетный листок"])

@app.get("/")
async def root():
    return {"message": "Hello World!"}