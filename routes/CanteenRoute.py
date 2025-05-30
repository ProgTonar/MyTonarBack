from fastapi import APIRouter, Depends

from database import get_db
from sqlalchemy.orm import Session
from service.CanteenService import CanteenService
from schemas.CanteenSchema import GetReceipt, CreateMenu
from schemas.BaseSchema import RessponseMessage
from typing import List

router = APIRouter()

def get_canteen_service(db: Session = Depends(get_db)):
  return CanteenService(db)

@router.get('/receipt/date/get', summary='Получение чеков по датам')
async def get_receipt_date(data: GetReceipt = Depends(), service: CanteenService = Depends(get_canteen_service)):
    return await service.get_receipt_date(data)

@router.get('/receipt/now/get/{login}', summary='Получение чеков за сегодня')
async def get_receipt_now(login: int, service: CanteenService = Depends(get_canteen_service)):
    return await service.get_receipt_now(login)

@router.post('/menu/create', response_model=RessponseMessage, summary='Создание меню')
async def create_menu(foods: list[CreateMenu], service: CanteenService = Depends(get_canteen_service)):
    return await service.create_menu(foods)

@router.get('/menu/today/get', summary='Получение меню столовой')
async def get_menu_today(service: CanteenService = Depends(get_canteen_service)):
    return await service.get_menu_today()

@router.get('/food/score/create', summary='Создание оценки блюда')
async def get_menu_today(service: CanteenService = Depends(get_canteen_service)):
    return await service.get_menu_today()