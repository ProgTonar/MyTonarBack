from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.bus_navigate import BusNavigateService
from schemas.bus_navigate import BusNavigate, BusNavigateCreate, BusNavigateUpdate
from typing import List

router = APIRouter(prefix="/bus-navigates", tags=["bus-navigates"])

@router.post("/", response_model=BusNavigate)
async def create_bus_navigate(
    bus_navigate: BusNavigateCreate,
    db: AsyncSession = Depends(get_db)
):
    service = BusNavigateService(db)
    return await service.create(bus_navigate)

@router.get("/{bus_navigate_id}", response_model=BusNavigate)
async def get_bus_navigate(
    bus_navigate_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = BusNavigateService(db)
    bus_navigate = await service.get_by_id(bus_navigate_id)
    if not bus_navigate:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return bus_navigate

@router.get("/", response_model=List[BusNavigate])
async def get_all_bus_navigates(
    db: AsyncSession = Depends(get_db)
):
    service = BusNavigateService(db)
    return await service.get_all()

@router.put("/{bus_navigate_id}", response_model=BusNavigate)
async def update_bus_navigate(
    bus_navigate_id: int,
    bus_navigate_data: BusNavigateUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = BusNavigateService(db)
    bus_navigate = await service.update(bus_navigate_id, bus_navigate_data)
    if not bus_navigate:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return bus_navigate

@router.delete("/{bus_navigate_id}")
async def delete_bus_navigate(
    bus_navigate_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = BusNavigateService(db)
    if not await service.delete(bus_navigate_id):
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return {"message": "Маршрут удален успешно"}

@router.post("/{bus_navigate_id}/stops/{stop_id}", response_model=BusNavigate)
async def add_stop_to_bus_navigate(
    bus_navigate_id: int,
    stop_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = BusNavigateService(db)
    bus_navigate = await service.add_stop(bus_navigate_id, stop_id)
    if not bus_navigate:
        raise HTTPException(status_code=404, detail="Маршрут или остановка не найдены")
    return bus_navigate 
