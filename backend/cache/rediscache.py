import asyncio

import aioredis
from .basecache import Cache


class RedisCache(Cache):
    """This is Redis cache implementation. This is used to store
    data in a Redis cache. It is an option for the cache handler.
    Use this if you have limited memory and want to use a persistent
    cache. You can also use this if you want cache and database to be
    in different servers and not on the same server the API is running on.

            data = self._connection["company_name"]
            summary = data[0]

    """

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
        """Get the value of the specified key from the cache."""
        futures = self._connection.get(key)
        data = await asyncio.gather(*futures)
        if None in data:
            return None
        return tuple(data)

    async def delete(self, key: str) -> bool:
        """Deletes specified company from the cache."""
        future_task = self._connection.delete(key)
        try:
            await asyncio.gather(future_task)
        except Exception:
            return False
        else:
            return True

    async def set(self, key: str, summary: str):
        """set the summary and date updated of a comany in the cache."""
        future_task = self._connection.set(key, summary)
        await asyncio.gather(future_task)

    async def purge(self):
        """Purge the entire cache."""
        future_task = self._connection.flushall()
        try:
            await asyncio.gather(future_task)
        except Exception:
            return False
        else:
            return True

    async def cleanup(self):
        """Close the connection to the cache."""
        return await self._connection.close()


_DRIVER = RedisCache
_DRIVER_TYPE = "REDIS"
