import time
import asyncio
from functools import wraps, partial


def ticktock(func):
    """This is a utility decorator that will time a function
    and print the time it took to run the function. This is useful
    for debugging and testing.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"{func.__name__} took {t2 - t1} seconds")
        return result

    return wrapper


# make a decorator that will time async functions
def ticktock_async(func):
    """This is the same as ticktock, but for async functions
    as well. Using @ticktock will not work for async functions.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        t1 = time.time()
        result = await func(*args, **kwargs)
        t2 = time.time()
        print(f"{func.__name__} took {t2 - t1} seconds")
        return result

    return wrapper


def executor(loop: asyncio.AbstractEventLoop = None, thread_pool_executor=None):
    """This is a decorator that allows you to run a function in a thread pool executor.
    This is useful for blocking functions that you don't want to block the event loop.
    This executor runs the code insdie the asyncio event loop. Either it's the existing
    loop or it will create a new loop for the function.
    """

    def decorator(func):
        """This is the decorator that will run the function in a thread pool executor."""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal loop, thread_pool_executor
            partials = partial(func, *args, **kwargs)
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(thread_pool_executor, partials)

        return wrapper

    return decorator
