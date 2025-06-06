from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.BusSchema import BusRouteSchema, BusRouteUpdateSchema, StopCreateSchema, StopUpdateSchema, AddStopToRoute
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

@router.put("/route/update", response_model=RessponseMessage)
async def update_route(data: BusRouteUpdateSchema, service: BusService = Depends(get_bus_service)):
    return await service.update_route(data)

@router.delete("/route/delete/{route_id}", response_model=RessponseMessage)
async def delete_route(route_id: int, service: BusService = Depends(get_bus_service)):
    return await service.delete_route(route_id)

@router.post("/stop/create")
async def create_stop(data: StopCreateSchema, service: BusService = Depends(get_bus_service)):
    return await service.create_stop(data)

@router.get("/stop/detail/{stop_id}")
async def get_stop_detail(stop_id: int, service: BusService = Depends(get_bus_service)):
    return await service.get_stop_detail(stop_id)

@router.delete("/stop/delete/{stop_id}")
async def delete_stop(stop_id: int, service: BusService = Depends(get_bus_service)):
    return await service.delete_stop(stop_id)

@router.put("/stop/update")
async def update_stop(data: StopUpdateSchema, service: BusService = Depends(get_bus_service)):
    return await service.update_stop(data)

@router.post("/stop/add-to/route")
async def add_stop_to_route(data: AddStopToRoute, service: BusService = Depends(get_bus_service)):
    return await service.add_stop_to_route(data)

@router.delete("/stop/{stop_id}/delete-from/route/{route_id}")
async def delete_stop_from_route(stop_id: int, route_id: int, service: BusService = Depends(get_bus_service)):
    return await service.delete_stop_from_route(stop_id, route_id)
