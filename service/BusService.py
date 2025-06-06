from schemas.BusSchema import BusRouteSchema, BusRouteUpdateSchema, StopCreateSchema, AddStopToRoute
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
        raw_route = self.db.get(BusRoute, route_id)

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
        
        db_route.title = data.title
        db_route.name_start = data.name_start
        db_route.name_end = data.name_end
        db_route.dots_start = data.dots_start.model_dump()
        db_route.dots_end = data.dots_end.model_dump()
        
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
    
    async def get_stop_detail(self, stop_id: int):
        db_stop = self.db.get(BusStop, stop_id)

        if not db_stop:
            raise HTTPException(status_code=409, detail='Такой остановки не существует')
        
        stop = {
            "id": db_stop.id,
            "name": db_stop.name,
            "time": db_stop.arrival_time,
            "coordinate": db_stop.coordinate,
        }

        return stop
    
    async def delete_stop(self, stop_id: int):
        db_stop = self.db.query(BusStop).filter(BusStop.id == stop_id).first()

        if not db_stop:
            raise HTTPException(status_code=409, detail='Такой остановки не существует')
        
        self.db.delete(db_stop)
        self.db.commit()

        return RessponseMessage(message='Остановка успешно удалена')
    
    async def update_stop(self, data: StopCreateSchema):
        db_stop = self.db.query(BusStop).filter(BusStop.id == data.id).first()

        if not db_stop:
            raise HTTPException(status_code=409, detail='Такой остановки не существует')
        
        db_stop.name = data.name
        db_stop.arrival_time = data.time
        db_stop.coordinate = data.coordinate.model_dump()
                
        self.db.commit()

        return RessponseMessage(message='Остановка успешно обновлена')
    
    async def add_stop_to_route(self, data: AddStopToRoute):
        db_route = self.db.get(BusRoute, data.route_id)
        db_stop = self.db.get(BusStop, data.stop_id)
        
        if not db_stop or not db_route:
            raise HTTPException(status_code=404, detail='Остановка или маршрут не найдены')
        
        if db_stop in db_route.stops:
            raise HTTPException(status_code=409, detail='Остановка уже добавлена к маршруту')

        db_route.stops.append(db_stop)
        self.db.commit()
            
        return RessponseMessage(message='Остановка успешно обновлена')
    
    async def delete_stop_from_route(self, route_id: int, stop_id: int):
        db_route = self.db.get(BusRoute, route_id)
        db_stop = self.db.get(BusStop, stop_id) 

        if not db_stop or not db_route:
            raise HTTPException(status_code=404, detail='Остановка или маршрут не найдены')
        
        if db_stop not in db_route.stops:
            raise HTTPException(status_code=409, detail='Остановка не привязана к маршруту')

        db_route.stops.remove(db_stop)
        self.db.commit()

        return RessponseMessage(message='Остановка успешно удалена из маршрута')
