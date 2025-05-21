from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.stop import Stop
from app.schemas.stop import StopCreate, StopUpdate
from typing import List, Optional
from datetime import datetime

class StopService:
    def __init__(self, db: AsyncSession):
        self.db = db

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