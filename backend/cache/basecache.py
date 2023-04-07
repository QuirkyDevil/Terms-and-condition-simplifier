class Cache:
    """Skeleton for cache handlers. Cache handlers are used to
    store data in a cache. This is used to store data that is
    frequently accessed. This is similar to the database handlers,
    except this can also just be a regular dictionary or redis cache.
    It should be implemented only if you want to have a cache. The API
    will work without a cache. If you use NGINX, you can use NGINX to
    cache the data instead of using internal cache. Some other ways of
    caching data are using a CDN or a reverse proxy. One of the good caching
    option if cloudflare. You can use cloudflare to cache the data.

        cache_format = {"company_name": ("summary", "last_updated")}


    """

    # a base cache handler
    def __init__(self):
        self._connection = None  # this is similar
        # to the database handlers, except this can also just
        # be a regular dictionary

    async def connect(self, *args, **kwargs):
        """base cache connect method. This method should be implemented"""
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        """base cache get method. This method should be implemented"""
        raise NotImplementedError

    async def set(self, *args, **kwargs):
        """base cache set method. This method should be implemented"""
        raise NotImplementedError

    async def delete(self, *args, **kwargs) -> int:
        """base cache delete method. This method should be implemented"""
        raise NotImplementedError

    async def cleanup(self):
        """base cache cleanup method. This method should be implemented"""
        raise NotImplementedError
