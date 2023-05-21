# Quick Jumpstart

## How to use the API directy

```py
import aiohttp
import asyncio
async def main():
    session = aiohttp.ClientSession()
    resp = await session.get("http://localhost:8000/get_summary/?comapny=google")
    returned_data = await resp.json()
    print(returned_data)
    await session.close()
asyncio.get_event_loop().run_until_complete(main())
```

```sh
>>> {'status': 200, 'data': 'This is a sample summary'}
```

## Install The Extension

- [Chrome](https://chrome.google.com/webstore/category/extensions)