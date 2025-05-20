from fastapi import APIRouter
from app.api import contacts, bus_navigate, stop

api_router = APIRouter()
api_router.include_router(contacts.router)
api_router.include_router(bus_navigate.router)
api_router.include_router(stop.router)
