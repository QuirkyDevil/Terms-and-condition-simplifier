import asyncio
import functools


def executor(loop: asyncio.AbstractEventLoop = None, thread_pool_executor=None):
    """This is a decorator that allows you to run a function in a thread pool executor.
    This is useful for blocking functions that you don't want to block the event loop.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal loop, thread_pool_executor
            partial = functools.partial(func, *args, **kwargs)
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(thread_pool_executor, partial)

        return wrapper

    return decorator
