from typing import Dict

from .basecache import Cache


class InMemoryCache(Cache):
    """This is an in-memory cache handler. This is used to store
    data in a dictionary. This is used to store data that is frequently
    accessed. This stores the company name, summary, and the date it was
    last updated. This is used to store data that is frequently accessed.
    It stores the dictionary in memory, so it is not persistent. It stores
    summary and last updated date in the dictionary as tuples.
    """

    async def connect(self, **kwargs):
        """Connect to the cache and return the connection instance"""
        # to keep it consistent we will indeed have an async function
        # to just register a dict
        self._connection: Dict[str, str] = {}
        max_size = kwargs["max_cache_size"]
        self._max_size = max_size
        return self._connection

    async def get(self, key: str):
        """Return the summary and time last updated from the cache"""
        summary = self._connection.get(key)
        data = (key, summary)
        if None in data:
            return None
        return data

    async def update(self, key: str, summary: str):
        """Updates the summary and time last updated in the cache"""
        self._connection[key] = summary

    async def delete(self, key: str) -> bool:
        """Delete a document in the cache and return whether the delete succeeded or failed"""
        try:
            self._connection.pop(key)
            self._connection.pop(key) # safe side to make sure it's deleted
        except KeyError:
            return False  # failed
        return True  # success

    async def purge(self):
        """Purge the cache"""
        self._connection.clear()

    async def set(self, key: str, summary: str):
        """Set the summary and time last updated in the cache"""
        self._connection[key] = summary

    async def list_all(self):
        """List all the keys in the cache"""
        return self._connection

    async def cleanup(self):
        """Cleanup the cache. Believe it or not, there is a 
        cleanup operation for a dictionary.
        """
        # believe it or not
        # there is a cleanup operation for a dictionary
        # we'll free the memory by clearing the dictionary
        self._connection.clear()


_DRIVER = InMemoryCache
_DRIVER_TYPE = "MEMORY"
