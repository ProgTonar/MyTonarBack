from fastapi import APIRouter, Depends
from service.MoneyService import MoneyService
from schemas.MoneySchema import MoneySchema
from service.MoneyService import MoneyService

router = APIRouter()

def get_money_service():
    return MoneyService()

@router.get('/get/{login}', response_model=MoneySchema, summary='Получение расчетного листа')
async def get_money(login: int,service: MoneyService = Depends(get_money_service)):
    return await service.get_money(login)

