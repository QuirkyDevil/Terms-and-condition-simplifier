from typing import Dict

from .basecache import Cache


class InMemoryCache(Cache):
    """cache summary of terms and condition in the memory and not query the database every time"""

    async def connect(self, **kwargs):
        # to keep it consistent we will indeed have an async function
        # to just register a dict
        self._connection: Dict[str, str] = {}
        max_size = kwargs["max_cache_size"]
        self._max_size = max_size
        return self._connection

    async def get(self, key: str):
        summary = self._connection.get(key)
        data = (key, summary)
        if None in data:
            return None
        return data

    async def update(self, key: str, summary: str):
        self._connection[key] = summary

    async def delete(self, key: str) -> bool:
        try:
            self._connection.pop(key)
            self._connection.pop(key)
        except KeyError:
            return False  # failed
        return True  # success

    async def purge(self):
        self._connection.clear()

    async def set(self, key: str, summary: str):
        self._connection[key] = summary

    async def cleanup(self):
        # believe it or not
        # there is a cleanup operation for a dictionary
        # we'll free the memory by clearing the dictionary
        self._connection.clear()


_DRIVER = InMemoryCache
_DRIVER_TYPE = "MEMORY"
