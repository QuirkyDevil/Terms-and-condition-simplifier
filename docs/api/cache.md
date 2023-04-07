```{eval-rst}
Base Cache Class
--------------------
.. automodule:: backend.cache.basecache
   :members:
   :undoc-members:
   :show-inheritance:

Redis Caching
--------------------
.. automodule:: backend.cache.rediscache
   :members:
   :undoc-members:
   :show-inheritance:

Memory Caching
--------------------
.. automodule:: backend.cache.memorycache
   :members:
   :undoc-members:
   :show-inheritance:
```

# Custom Caching system
If you want to have custom implementation of caching, or have some other cache which is better than redis or memory
cache which is provided, u are free to do so. For that u can derive your custom class from `cache` class. It provides
with base methods which are **_compulsary_** to implement.
- To get it working first make your own caching system with the methods `cleanup()`, `connect()`, `delete()`, `set()` and `get()`
- Aftee u have the caching system code ready andworking all fine. It is time to implement it in API.