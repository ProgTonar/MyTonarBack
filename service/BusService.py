from schemas.BusSchema import BusRouteSchema, BusRouteUpdateSchema, StopCreateSchema
from fastapi import HTTPException
from models import BusRoute, BusStop
from schemas.BaseSchema import RessponseMessage
from sqlalchemy.orm import Session 


class BusService:
    def __init__(self, db: Session):
        self.db = db

    async def create_bus_route(self, data: BusRouteSchema):
        db_route = self.db.query(BusRoute).filter(BusRoute.title == data.title).first()

        if db_route:
            raise HTTPException(status_code=409, detail="Маршрут с таким названием уже существует")

        bus_route = BusRoute(
            title=data.title,
            name_start=data.name_start,
            name_end=data.name_end,
            dots_start={"x": data.dots_start.x, "y": data.dots_start.y},
            dots_end={"x": data.dots_end.x, "y": data.dots_end.y}
        )
        self.db.add(bus_route)
        self.db.commit()

        self.db.commit()
        return RessponseMessage(message='Маршрут успешно создан')

    async def get_route_detail(self, route_id: int):
        raw_route = self.db.query(BusRoute).filter(BusRoute.id == route_id).first()

        stops = raw_route.stops

        route = {
            "title": raw_route.title,
            "name_start": raw_route.name_start,
            "name_end": raw_route.name_end,
            "dots_start": raw_route.dots_start,
            "dots_end": raw_route.dots_end,
            "stops": stops
        }

        return route

    async def get_all_routes(self):
        raw_routes = self.db.query(BusRoute).all()

        routes = []

        for item in raw_routes:
            routes.append({
                "title": item.title,
                "name_start": item.name_start,
                "name_end": item.name_end,
                "dots_start": item.dots_start,
                "dots_end": item.dots_end,
            })

        return routes 

    async def update_route(self, data: BusRouteUpdateSchema):
        db_route = self.db.query(BusRoute).filter(BusRoute.id == data.id).first()

        if not db_route:
            raise HTTPException(status_code=404, detail="Маршрут не найден")
        
        update_data = data.model_dump(exclude_unset=True)
        
        update_data.pop('id', None)
        
        for field, value in update_data.items():
            setattr(db_route, field, value)
        
        self.db.commit()
        
        return RessponseMessage(message='Маршрут успешно обновлен')

    async def delete_route(self, route_id: int):
        db_route = self.db.query(BusRoute).filter(BusRoute.id == route_id).first()

        if not db_route:
            raise HTTPException(status_code=404, detail='Маршрут не найден')

        self.db.delete(db_route)
        self.db.commit()

        return RessponseMessage(message='Маршрут успешно удален')

    async def create_stop(self, data: StopCreateSchema):
        db_stop = self.db.query(BusStop).filter(BusStop.name == data.name).first()

        if db_stop:
            raise HTTPException(status_code=409, detail='Остановка с таким именем уже существует')
        
        new_stop = BusStop(name=data.name, arrival_time=data.time, coordinate={"x": data.coordinate.x, "y": data.coordinate.y})

        self.db.add(new_stop)
        self.db.commit()

        return RessponseMessage(message='Остановка успешно создана')
    
    async def delete_stop(self, stop_id: int):
        db_stop = self.db.query(BusStop).filter(BusStop.name == stop_id).first()

        if not db_stop:
            raise HTTPException(status_code=409, detail='Такой остановки не существует')
        
        self.db.delete(db_stop)
        self.db.commit()

        return RessponseMessage(message='Остановка успешно удалена')
#         
    
#     async def create(self, stop: StopCreate) -> Stop:
#         db_stop = Stop(
#             name=stop.name,
#             arrival_time=stop.arrival_time,
#             coordinate={"x": stop.coordinate.x, "y": stop.coordinate.y}
#         )
#         self.db.add(db_stop)
#         await self.db.commit()
#         await self.db.refresh(db_stop)
#         return db_stop

#     async def get_by_id(self, stop_id: int) -> Optional[Stop]:
#         query = select(Stop).where(Stop.id == stop_id)
#         result = await self.db.execute(query)
#         return result.scalar_one_or_none()

#     async def get_all(self) -> List[Stop]:
#         query = select(Stop)
#         result = await self.db.execute(query)
#         return result.scalars().all()

#     async def update(self, stop_id: int, stop_data: StopUpdate) -> Optional[Stop]:
#         db_stop = await self.get_by_id(stop_id)
#         if not db_stop:
#             return None

#         update_data = stop_data.model_dump(exclude_unset=True)
        

#         if "coordinate" in update_data:
#             update_data["coordinate"] = {"x": update_data["coordinate"].x, "y": update_data["coordinate"].y}

#         for key, value in update_data.items():
#             setattr(db_stop, key, value)
        
#         db_stop.updated_at = datetime.utcnow()
#         await self.db.commit()
#         await self.db.refresh(db_stop)
#         return db_stop

#     async def delete(self, stop_id: int) -> bool:
#         db_stop = await self.get_by_id(stop_id)
#         if not db_stop:
#             return False
        
#         await self.db.delete(db_stop)
#         await self.db.commit()
#         return True 