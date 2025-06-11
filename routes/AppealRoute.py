from fastapi import APIRouter, Depends

from database import get_db
from sqlalchemy.orm import Session
from service.AppealService import AppealService
from schemas.AppealSchema import CreateAppeal, AddAnswer, ChangeActive, PutLike
from schemas.BaseSchema import RessponseMessage

router = APIRouter()

def get_appeal_service(db: Session = Depends(get_db)):
  return AppealService(db)

@router.post('/create', response_model=RessponseMessage)
async def create_appeal(data: CreateAppeal, service: AppealService = Depends(get_appeal_service)):
    return await service.create_appeal(data)

@router.get('/detail/{appeal_id}')
async def get_appeal_detail(appeal_id: int, service: AppealService = Depends(get_appeal_service)):
    return await service.get_appeal_detail(appeal_id)

@router.get('/get/all')
async def get_all_appeal(service: AppealService = Depends(get_appeal_service)):
    return await service.get_all_appeal()

@router.patch('/add/answer', response_model=RessponseMessage)
async def add_answer_appeal(data: AddAnswer,service: AppealService = Depends(get_appeal_service)):
    return await service.add_answer_appeal(data)

@router.delete('/delete/{appeal_id}', response_model=RessponseMessage)
async def delete_appeal(appeal_id: int,service: AppealService = Depends(get_appeal_service)):
    return await service.delete_appeal(appeal_id)

@router.get('/get/statuses')
async def get_statuses_appeal(service: AppealService = Depends(get_appeal_service)):
    return await service.get_statuses_appeal()

@router.patch('/change/status', response_model=RessponseMessage)
async def change_active_appeal(data: ChangeActive,service: AppealService = Depends(get_appeal_service)):
    return await service.change_active_appeal(data)

@router.post('/put/like', response_model=RessponseMessage)
async def put_like(data: PutLike,service: AppealService = Depends(get_appeal_service)):
    return await service.put_like(data)
