import importlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from typing import Tuple


import config as settings


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ALLOWED_ORIGINS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.cache = None
app.DB = None

if settings.ENFORCE_SECURE_SCHEME:
    app.add_middleware(HTTPSRedirectMiddleware)


def _check_driver() -> Tuple[type, str]:
    """"""
    _driver_path = settings.DATABASE_DRIVERS["driver"]
    # import "driver" path of db from config.py and import it using
    # importlib.import_module
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)


def _check_cache_driver() -> Tuple[type, str]:
    """"""
    _driver_path = settings.CACHE_DRIVERS["driver"]
    # import "driver" path of cache from config.py and import it using
    # importlib.import_module
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)


# on startup
@app.on_event("startup")
async def startup_event():
    driver_class, _ = _check_driver()
    config = settings.DATABASE_DRIVERS["config"]
    driver = driver_class()
    await driver.connect(**config)
    cache_driver_class, _ = _check_cache_driver()
    cache_config = settings.CACHE_DRIVERS["config"]
    cache_driver = cache_driver_class()

    cache_config["max_cache_size"] = settings.MAX_CACHE_SIZE  # we pass this into
    # the connect function of the cache driver regardless whether its the
    # memory cache driver or not.
    await cache_driver.connect(**cache_config)

    app.DB = driver
    app.cache = cache_driver


# on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    # disconnect from databases and close caches.
    try:
        await app.DB.cleanup()
        await app.cache.cleanup()
    except Exception as e:
        # disregard any errors that may occur during shutdown.
        pass


@app.get("/")
async def read_root() -> JSONResponse:
    """Root endpoint."""
    return {"Hello": "World"}


@app.get("/get")
async def get_summary(query: str) -> JSONResponse:
    """Search endpoint."""
    result = await app.DB.get(query)
    if result:
        return JSONResponse(content=result, status_code=200)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/search")
async def search_summary(query: str) -> JSONResponse:
    """Search endpoint."""
    result = await app.DB.search(query)
    if result:
        return JSONResponse(content=result, status_code=200)
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/delete")
async def delete(query: str, secret_key: str) -> JSONResponse:
    """Delete endpoint."""
    if secret_key != settings.SECRET_KEY:
        return {"error": "unauthorized"}
    db_deleted = await app.DB.delete(query)
    cahce_Deleted = await app.cache.delete(query)
    status_codes = 204
    if db_deleted is False or cahce_Deleted or False:
        status_codes = 500
    return JSONResponse(content=None, status_code=status_codes)
