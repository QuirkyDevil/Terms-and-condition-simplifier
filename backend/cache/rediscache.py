import asyncio

import aioredis
from .basecache import Cache


class RedisCache(Cache):
    """Redis cache driver."""

    async def connect(self, **kwargs):
        """Connect to the redis server."""
        connection_uri = kwargs["connection_uri"]
        username = kwargs.get("username")
        password = kwargs.get("password")

        extra_kwargs = {}
        if username and password:
            extra_kwargs["username"] = username
            extra_kwargs["password"] = password

        redis = aioredis.from_url(connection_uri, **extra_kwargs)
        self._connection = redis
        return self._connection

    async def get(self, key: str):
        """Get the value of a key from the cache."""
        futures = self._connection.get(key)
        data = await asyncio.gather(*futures)
        if None in data:
            return None
        return tuple(data)

    async def delete(self, key: str) -> bool:
        """Delete a key from the cache."""
        future_task = self._connection.delete(key)
        try:
            await asyncio.gather(future_task)
        except Exception:
            return False
        else:
            return True

    async def set(self, key: str, summary: str):
        """Set a key in the cache."""
        future_task = self._connection.set(key, summary)
        await asyncio.gather(future_task)

    async def cleanup(self):
        return await self._connection.close()


_DRIVER = RedisCache
_DRIVER_TYPE = "REDIS"
