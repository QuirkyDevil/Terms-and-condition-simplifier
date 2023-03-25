import asyncio
import datetime
import importlib
from typing import Tuple
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


from backend.functions.main import scrape_and_summarize
import backend.config as settings


app = FastAPI(title="Terms and Condition Simplifier", version="0.1.0 Alpha")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ALLOWED_ORIGINS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

analyzer = SentimentIntensityAnalyzer()

app.cache = None
app.DB = None

if settings.ENFORCE_SECURE_SCHEME:
    app.add_middleware(HTTPSRedirectMiddleware)


def _check_driver() -> Tuple[type, str]:
    """Check the driver provided in the config file and return the driver class and the driver type"""
    _driver_path = settings.DATABASE_DRIVERS["driver"]
    # import "driver" path of db from config.py and import it using
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)


def _check_cache_driver() -> Tuple[type, str]:
    """check the cache driver provided in the config file and return the driver class and the driver type"""
    _driver_path = settings.CACHE_DRIVERS["driver"]
    # import "driver" path of cache from config.py and import it using
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)


async def the_process():
    ...


# on startup
@app.on_event("startup")
async def startup_event():
    """This function is called on startup and connects to the database and cache"""
    driver_class, _ = _check_driver()
    config = settings.DATABASE_DRIVERS["config"]
    driver = driver_class()
    await driver.connect(**config)

    cache_driver_class, _ = _check_cache_driver()
    cache_config = settings.CACHE_DRIVERS["config"]
    cache_driver = cache_driver_class()
    cache_config["max_cache_size"] = settings.MAX_CACHE_SIZE
    await cache_driver.connect(**cache_config)

    app.DB = driver
    app.cache = cache_driver


# on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """This function is called on shutdown and disconnects from the database and cache"""
    # disconnect from databases and close caches.
    try:
        await app.DB.cleanup()
        await app.cache.cleanup()
    except Exception as e:
        # disregard any errors that may occur during shutdown.
        pass


@app.get("/", tags=["Health Check"])
async def read_root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse(
        content={"message": "Welcome to Terms and Condition simplifier API"},
        status_code=200,
    )


@app.get("/ping", tags=["Health Check"])
async def ping() -> JSONResponse:
    """Ping."""
    return JSONResponse(content={"message": "pong"}, status_code=200)


@app.get("/get_summary", tags=["general"])
async def get_summary(company: str) -> JSONResponse:
    """Search."""
    check_cache = await app.cache.get(company)
    if not check_cache:
        check_db = await app.DB.search(company)
        if check_db:
            await app.cache.set(company, check_db[1])
            return JSONResponse(content=check_db, status_code=200)
        else:
            result = await scrape_and_summarize(analyzer, company)
            if result:
                await app.DB.add(company, result, datetime.datetime.now())
                await app.cache.set(company, result)
                return {"status": 200, "data": result}
            raise HTTPException(status_code=404, detail="Company Not Found!")
    return JSONResponse(content=check_cache, status_code=200)


@app.get("/search_summary", tags=["general"])
async def search_summary(company: str) -> JSONResponse:
    """Search."""
    result = await app.DB.search(company)
    if result:
        return JSONResponse(content=result, status_code=200)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/list_all", tags=["general"])
async def list_companies() -> JSONResponse:
    result = await app.cache.list_all()
    if result:
        return {"status": "success", "data": result}
    raise HTTPException(status_code=404, detail="No items found")


@app.get("/add_company", tags=["general"])
async def add(company: str) -> JSONResponse:
    """Add."""
    result = await scrape_and_summarize(analyzer, company)
    if result:
        await app.DB.add(company, result, datetime.datetime.now())
        data = (result, datetime.datetime.now())
        await app.cache.set(company, data)
        return JSONResponse(content=result, status_code=200)
    raise HTTPException(status_code=404, detail="Company Not Found!")


@app.post("/purge_cache", tags=["admin"])
async def purge_cache(secret_key: str) -> JSONResponse:
    if secret_key != settings.SECRET_KEY:
        return JSONResponse(content={"error": "unauthorized"}, status_code=401)
    await app.cache.purge()
    return JSONResponse(content="Purged", status_code=200)


@app.put("/update", tags=["admin"])
async def update(company: str, secret_key: str) -> JSONResponse:
    if secret_key != settings.SECRET_KEY:
        return JSONResponse(content={"error": "unauthorized"}, status_code=401)
    summary = await scrape_and_summarize(analyzer, company)
    db_updated = await app.DB.update(company, summary, datetime.datetime.now())
    cache_updated = await app.cache.update(company, summary)
    status_codes = 204
    if db_updated is False or cache_updated is False:
        status_codes = 500
    return JSONResponse(content=None, status_code=status_codes)


@app.delete("/delete", tags=["admin"])
async def delete(company: str, secret_key: str) -> JSONResponse:
    """Delete."""
    if secret_key != settings.SECRET_KEY:
        return JSONResponse(content={"error": "unauthorized"}, status_code=401)
    db_deleted = await app.DB.delete(company)
    cache_Deleted = await app.cache.delete(company)
    status_codes = 204
    if db_deleted is False or cache_Deleted or False:
        status_codes = 500
    return JSONResponse(content=None, status_code=status_codes)
