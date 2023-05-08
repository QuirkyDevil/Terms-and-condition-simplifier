import datetime
import importlib
from typing import Tuple
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


from backend.functions.main import scrape_and_summarize, summerize_usertext

import backend.config as settings

from playwright.async_api import async_playwright, Playwright


app = FastAPI(title="Terms and Condition Simplifier", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ALLOWED_ORIGINS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.cache = None
app.DB = None
playwright: Playwright = None
browser = None

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


# on startup
@app.on_event("startup")
async def startup_event():
    """This function is called on startup and connects to the database and cache"""
    global browser, playwright  # skipcq: PYL-W0603
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
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
    except Exception:
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
            await app.cache.set(company, check_db[1], check_db[2], check_db[3])
            return {
                "status": 200,
                "data": {
                    "summary": check_db[1],
                    "date": check_db[2],
                    "link": check_db[3],
                    "source": "db",
                },
            }
        else:
            result = await scrape_and_summarize(browser, company)
            if result:
                await app.DB.add(company, result[0], datetime.datetime.now(), result[1])
                await app.cache.set(
                    company, result[0], datetime.datetime.now(), result[1]
                )
                return {
                    "status": 200,
                    "data": {
                        "summary": result[0],
                        "date": datetime.datetime.now(),
                        "link": result[1],
                        "source": "scrape",
                    },
                }
            raise HTTPException(status_code=404, detail="Company Not Found!")
    return {
        "status": 200,
        "data": {
            "summary": check_cache[0],
            "date": check_cache[1],
            "link": check_cache[2],
            "source": "cache",
        },
    }


@app.get("/search_summary", tags=["general"])
async def search_summary(company: str) -> JSONResponse:
    """Search."""
    result = await app.cache.get(company)
    if result:
        return {
            "status": 200,
            "data": {
                "summary": result[0],
                "date": result[1],
                "link": result[2],
                "source": "cache",
            },
        }
    result = await app.DB.search(company)
    if result:
        await app.cache.set(company, result[1], result[2], result[3])
        return {
            "status": 200,
            "data": {
                "summary": result[1],
                "date": result[2],
                "link": result[3],
                "source": "db",
            },
        }
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/list_db", tags=["general"])
async def list_companies() -> JSONResponse:
    result = await app.DB.list_all()
    if result:
        return {"status": 200, "data": result}
    raise HTTPException(status_code=404, detail="No items found")


@app.get("/list_cache", tags=["general"])
async def list_cache() -> JSONResponse:
    """List all items in cache."""
    result = await app.cache.list_all()
    if result:
        return {"status": 200, "data": result}
    raise HTTPException(status_code=404, detail="No items found")


@app.post("/user_summary", tags=["general"])
async def user_summary(text: str) -> JSONResponse:
    """Give summary of provided text/t&c by user."""
    result = await summerize_usertext(text)
    if result:
        return {"status": 200, "data": result}
    raise HTTPException(status_code=404, detail="Error while generating summary")


@app.post("/purge_cache", tags=["admin"])
async def purge_cache(secret_key: str) -> JSONResponse:
    """Purge entire cache."""
    if secret_key != settings.SECRET_KEY:
        return JSONResponse(content={"error": "unauthorized"}, status_code=401)
    await app.cache.purge()
    return JSONResponse(content="Purged", status_code=200)


@app.post("/purge_db", tags=["admin"])
async def purge_db(secret_key: str) -> JSONResponse:
    """Purge entire database."""
    if secret_key != settings.SECRET_KEY:
        return JSONResponse(content={"error": "unauthorized"}, status_code=401)
    await app.DB.purge()
    return JSONResponse(content="Purged", status_code=200)


@app.put("/update", tags=["admin"])
async def update(company: str, secret_key: str) -> JSONResponse:
    """Update Terms and condition summary of a company."""
    if secret_key != settings.SECRET_KEY:
        return JSONResponse(content={"error": "unauthorized"}, status_code=401)
    summary = await scrape_and_summarize(browser, company)
    db_updated = await app.DB.update(
        company, summary[0], datetime.datetime.now(), summary[1]
    )
    cache_updated = await app.cache.update(company, summary)
    status_codes = 204
    if db_updated is False or cache_updated is False:
        status_codes = 500
    return {"status": status_codes, "data": summary}


@app.delete("/delete", tags=["admin"])
async def delete(company: str, secret_key: str) -> JSONResponse:
    """Deletes a company from the database and cache."""
    if secret_key != settings.SECRET_KEY:
        return {"error": "unauthorized"}
    db_deleted = await app.DB.delete(company)
    cache_Deleted = await app.cache.delete(company)
    status_codes = 204
    if db_deleted is False or cache_Deleted or False:
        status_codes = 500
    return {"status": status_codes, "data": "Deleted"}
