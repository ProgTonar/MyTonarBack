from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.BusSchema import BusRouteSchema, BusRouteUpdateSchema
from schemas.BaseSchema import RessponseMessage
from service.BusService import BusService

router = APIRouter()

def get_bus_service(db: Session = Depends(get_db)):
    return BusService(db)

@router.post("/route/create", response_model=RessponseMessage)
async def create_bus_route(data: BusRouteSchema, service: BusService = Depends(get_bus_service)):
    return await service.create_bus_route(data)

@router.get("/route/detail/{route_id}")
async def get_route_detail(route_id: int, service: BusService = Depends(get_bus_service)):
    return await service.get_route_detail(route_id)

@router.get("/routes/get")
async def get_all_routes(service: BusService = Depends(get_bus_service)):
    return await service.get_all_routes()

@router.patch("/route/update", response_model=RessponseMessage)
async def route_update(data: BusRouteUpdateSchema, service: BusService = Depends(get_bus_service)):
    return await service.route_update(data)

# @router.delete("/{bus_navigate_id}")
# async def delete_bus_navigate(
#     bus_navigate_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     service = BusNavigateService(db)
#     if not await service.delete(bus_navigate_id):
#         raise HTTPException(status_code=404, detail="Маршрут не найден")
#     return {"message": "Маршрут удален успешно"}

# @router.post("/{bus_navigate_id}/stops/{stop_id}", response_model=BusNavigate)
# async def add_stop_to_bus_navigate(
#     bus_navigate_id: int,
#     stop_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     service = BusNavigateService(db)
#     bus_navigate = await service.add_stop(bus_navigate_id, stop_id)
#     if not bus_navigate:
#         raise HTTPException(status_code=404, detail="Маршрут или остановка не найдены")
#     return bus_navigate 
