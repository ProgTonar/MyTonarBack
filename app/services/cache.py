import json
from datetime import datetime, timedelta
from typing import Any, Optional
from redis.asyncio import Redis
from fastapi import Request

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class RedisCache:
    def __init__(self, request: Request = None, redis_client: Optional[Redis] = None):
        self.redis: Optional[Redis] = redis_client or (request.app.state.redis if request else None)
    
    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return None
            
        cached_data = await self.redis.get(key)
        return json.loads(cached_data) if cached_data else None

    async def set(self, key: str, data: Any, ttl: int = 3600) -> None:
        if self.redis:
            await self.redis.setex(key, timedelta(seconds=ttl), json.dumps(data, cls=DateTimeEncoder))

    async def delete(self, *keys: str) -> None:
        if self.redis and keys:
            await self.redis.delete(*keys)

    async def invalidate_pattern(self, pattern: str) -> None:
        if self.redis:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)


async def get_cache(request: Request) -> RedisCache:
    return RedisCache(request)