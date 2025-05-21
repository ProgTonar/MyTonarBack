from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.stop import StopService
from app.schemas.stop import Stop, StopCreate, StopUpdate
from typing import List

router = APIRouter(prefix="/stops", tags=["stops"])

@router.post("/", response_model=Stop)
async def create_stop(
    stop: StopCreate,
    db: AsyncSession = Depends(get_db)
):
    service = StopService(db)
    return await service.create(stop)

@router.get("/{stop_id}", response_model=Stop)
async def get_stop(
    stop_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = StopService(db)
    stop = await service.get_by_id(stop_id)
    if not stop:
        raise HTTPException(status_code=404, detail="Остановка не найдена")
    return stop

@router.get("/", response_model=List[Stop])
async def get_all_stops(
    db: AsyncSession = Depends(get_db)
):
    service = StopService(db)
    return await service.get_all()

@router.put("/{stop_id}", response_model=Stop)
async def update_stop(
    stop_id: int,
    stop_data: StopUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = StopService(db)
    stop = await service.update(stop_id, stop_data)
    if not stop:
        raise HTTPException(status_code=404, detail="Остановка не найдена")
    return stop

@router.delete("/{stop_id}")
async def delete_stop(
    stop_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = StopService(db)
    if not await service.delete(stop_id):
        raise HTTPException(status_code=404, detail="Остановка не найдена")
    return {"message": "Остановка удалена успешно"} 