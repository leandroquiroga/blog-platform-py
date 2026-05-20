import json
from fastapi import HTTPException, status
from redis.asyncio import Redis
from typing import Any

class CacheUtils:

    def __init__(self, client: Redis | None):
        """Utility class for managing Redis cache."""
        self.client = client

    async def get_cache(self, key: str) -> dict | None:
        """Get cached data by key."""

        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Redis client not initialized",
            )

        data = await self.client.get(key)
        if data is None:
            return None

        return json.loads(data)

    async def set_cache(self, key: str, value: dict | list[dict[str, Any]], expire: int = 300) -> None:
        """ Set cache data """
        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Redis client not initialized",
            )
        await self.client.set(key, json.dumps(value), ex=expire)
        
    async def clear_cache(self, pattern: str) -> None:
        """ Clear cache by pattern """
        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Redis client not initialized",
            )
        keys = await self.client.keys(pattern)
        if keys:
            await self.client.delete(*keys)