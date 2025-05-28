from fastapi import APIRouter, Depends

from database import get_db
from sqlalchemy.orm import Session
from service.CanteenService import CanteenService
from schemas.CanteenSchema import GetReceipt, GetMenu

router = APIRouter()

def get_canteen_service(db: Session = Depends(get_db)):
  return CanteenService(db)

@router.get('/receipt/date/get')
async def get_receipt_date(data: GetReceipt = Depends(), service: CanteenService = Depends(get_canteen_service)):
    return await service.get_receipt_date(data)

@router.get('/receipt/now/get/{login}')
async def get_receipt_now(login: int, service: CanteenService = Depends(get_canteen_service)):
    return await service.get_receipt_now(login)

@router.get('/menu/get')
async def get_menu(menu: GetMenu, service: CanteenService = Depends(get_canteen_service)):
    return await service.get_menu(menu)
