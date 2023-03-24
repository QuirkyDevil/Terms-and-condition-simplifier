import time
from functools import wraps

def ticktock(func):
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
    @wraps(func)
    async def wrapper(*args, **kwargs):
        t1 = time.time()
        result = await func(*args, **kwargs)
        t2 = time.time()
        print(f"{func.__name__} took {t2 - t1} seconds")
        return result
    return wrapper

