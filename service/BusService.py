from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload
from models.bus_navigate import BusNavigate, stops_has_busnavigate
from models.stop import Stop
from schemas.BusSchema import BusNavigateCreate, BusNavigateUpdate
from typing import List, Optional
from datetime import datetime

class BusNavigateService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, bus_navigate: BusNavigateCreate) -> BusNavigate:
        # Создаем маршрут
        db_bus_navigate = BusNavigate(
            title=bus_navigate.title,
            name_start=bus_navigate.name_start,
            name_end=bus_navigate.name_end,
            dots_start={"x": bus_navigate.dots_start.x, "y": bus_navigate.dots_start.y},
            dots_end={"x": bus_navigate.dots_end.x, "y": bus_navigate.dots_end.y}
        )
        self.db.add(db_bus_navigate)
        await self.db.commit()
        await self.db.refresh(db_bus_navigate)

        # Если есть остановки, создаем их и связываем с маршрутом
        if bus_navigate.stops:
            for stop_data in bus_navigate.stops:
                # Создаем новую остановку
                db_stop = Stop(
                    name=stop_data.name,
                    arrival_time=stop_data.arrival_time,
                    coordinate={"x": stop_data.coordinate.x, "y": stop_data.coordinate.y}
                )
                self.db.add(db_stop)
                await self.db.commit()
                await self.db.refresh(db_stop)

                # Создаем связь
                stmt = insert(stops_has_busnavigate).values(
                    bus_navigate_id=db_bus_navigate.id,
                    stop_id=db_stop.id
                )
                await self.db.execute(stmt)

        await self.db.commit()
        return await self.get_by_id(db_bus_navigate.id)

    async def get_by_id(self, bus_navigate_id: int) -> Optional[BusNavigate]:
        query = select(BusNavigate).options(selectinload(BusNavigate.stops)).where(BusNavigate.id == bus_navigate_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[BusNavigate]:
        query = select(BusNavigate).options(selectinload(BusNavigate.stops))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, bus_navigate_id: int, bus_navigate_data: BusNavigateUpdate) -> Optional[BusNavigate]:
        db_bus_navigate = await self.get_by_id(bus_navigate_id)
        if not db_bus_navigate:
            return None

        # Обновляем основные поля маршрута
        update_data = bus_navigate_data.model_dump(exclude={'stops'}, exclude_unset=True)
        
        # Преобразуем координаты в нужный формат
        if "dots_start" in update_data:
            dots_start = update_data["dots_start"]
            if isinstance(dots_start, dict):
                update_data["dots_start"] = {"x": dots_start.get("x", 0), "y": dots_start.get("y", 0)}
            else:
                update_data["dots_start"] = {"x": dots_start.x, "y": dots_start.y}

        if "dots_end" in update_data:
            dots_end = update_data["dots_end"]
            if isinstance(dots_end, dict):
                update_data["dots_end"] = {"x": dots_end.get("x", 0), "y": dots_end.get("y", 0)}
            else:
                update_data["dots_end"] = {"x": dots_end.x, "y": dots_end.y}

        for key, value in update_data.items():
            setattr(db_bus_navigate, key, value)
        
        # Обрабатываем остановки, если они есть в запросе
        if bus_navigate_data.stops is not None:
            # Обработка удаления остановок
            stops_to_delete = [stop for stop in bus_navigate_data.stops if stop.should_delete and stop.id is not None]
            for stop in stops_to_delete:
                await self.db.execute(
                    delete(stops_has_busnavigate).where(
                        stops_has_busnavigate.c.bus_navigate_id == bus_navigate_id,
                        stops_has_busnavigate.c.stop_id == stop.id
                    )
                )

            # Обработка новых и существующих остановок
            for stop_data in bus_navigate_data.stops:
                if not stop_data.should_delete:
                    if stop_data.id is None:
                        # Создаем новую остановку
                        coordinate = stop_data.coordinate
                        if isinstance(coordinate, dict):
                            coordinate = {"x": coordinate.get("x", 0), "y": coordinate.get("y", 0)}
                        else:
                            coordinate = {"x": coordinate.x, "y": coordinate.y}

                        db_stop = Stop(
                            name=stop_data.name,
                            arrival_time=stop_data.arrival_time,
                            coordinate=coordinate
                        )
                        self.db.add(db_stop)
                        await self.db.commit()
                        await self.db.refresh(db_stop)

                        # Создаем связь
                        stmt = insert(stops_has_busnavigate).values(
                            bus_navigate_id=bus_navigate_id,
                            stop_id=db_stop.id
                        )
                        await self.db.execute(stmt)
                    else:
                        # Обновляем существующую остановку
                        stop_query = select(Stop).where(Stop.id == stop_data.id)
                        stop_result = await self.db.execute(stop_query)
                        db_stop = stop_result.scalar_one_or_none()
                        
                        if db_stop:
                            db_stop.name = stop_data.name
                            db_stop.arrival_time = stop_data.arrival_time
                            
                            coordinate = stop_data.coordinate
                            if isinstance(coordinate, dict):
                                coordinate = {"x": coordinate.get("x", 0), "y": coordinate.get("y", 0)}
                            else:
                                coordinate = {"x": coordinate.x, "y": coordinate.y}
                            
                            db_stop.coordinate = coordinate
                            db_stop.updated_at = datetime.utcnow()

        db_bus_navigate.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(db_bus_navigate)
        return await self.get_by_id(bus_navigate_id)

    async def delete(self, bus_navigate_id: int) -> bool:
        db_bus_navigate = await self.get_by_id(bus_navigate_id)
        if not db_bus_navigate:
            return False
        
        # Удаляем связи с остановками
        await self.db.execute(
            delete(stops_has_busnavigate).where(
                stops_has_busnavigate.c.bus_navigate_id == bus_navigate_id
            )
        )
        
        await self.db.delete(db_bus_navigate)
        await self.db.commit()
        return True

    async def add_stop(self, bus_navigate_id: int, stop_id: int) -> Optional[BusNavigate]:
        # Загружаем маршрут вместе со связанными остановками
        query = select(BusNavigate).options(selectinload(BusNavigate.stops)).where(BusNavigate.id == bus_navigate_id)
        result = await self.db.execute(query)
        db_bus_navigate = result.scalar_one_or_none()
        
        if not db_bus_navigate:
            return None

        # Загружаем остановку
        stop_query = select(Stop).where(Stop.id == stop_id)
        stop_result = await self.db.execute(stop_query)
        stop = stop_result.scalar_one_or_none()
        
        if not stop:
            return None

        # Добавляем связь через промежуточную таблицу
        stmt = insert(stops_has_busnavigate).values(
            bus_navigate_id=bus_navigate_id,
            stop_id=stop_id
        )
        await self.db.execute(stmt)
        await self.db.commit()
        
        # Перезагружаем объект с обновленными связями
        await self.db.refresh(db_bus_navigate)
        return db_bus_navigate 
    
    async def create(self, stop: StopCreate) -> Stop:
        db_stop = Stop(
            name=stop.name,
            arrival_time=stop.arrival_time,
            coordinate={"x": stop.coordinate.x, "y": stop.coordinate.y}
        )
        self.db.add(db_stop)
        await self.db.commit()
        await self.db.refresh(db_stop)
        return db_stop

    async def get_by_id(self, stop_id: int) -> Optional[Stop]:
        query = select(Stop).where(Stop.id == stop_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Stop]:
        query = select(Stop)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, stop_id: int, stop_data: StopUpdate) -> Optional[Stop]:
        db_stop = await self.get_by_id(stop_id)
        if not db_stop:
            return None

        update_data = stop_data.model_dump(exclude_unset=True)
        

        if "coordinate" in update_data:
            update_data["coordinate"] = {"x": update_data["coordinate"].x, "y": update_data["coordinate"].y}

        for key, value in update_data.items():
            setattr(db_stop, key, value)
        
        db_stop.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(db_stop)
        return db_stop

    async def delete(self, stop_id: int) -> bool:
        db_stop = await self.get_by_id(stop_id)
        if not db_stop:
            return False
        
        await self.db.delete(db_stop)
        await self.db.commit()
        return True 