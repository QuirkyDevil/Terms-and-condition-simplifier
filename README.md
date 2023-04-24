<h1 align="center">
<sub>
    <img src="https://www.cloudflare.com/static/e483f0dab463205cec2642ab111e81fc/cdn-global-hero-illustration.svg" height="36">
</sub>
&nbsp;
Terms and Conditions Simplifier
</h1>
<p align="center">
<sup>
    A simple API that simplifies Terms and Conditions documents by removing all the legal jargon and only keeping the important parts.
</sup>
<br>
</p>

---

This is an API which can also be used as extension supported by chromium based browsers that takes a Terms and Conditions document and simplifies it. It does this by removing all the legal jargon and only keeping the important parts. It also removes all the unnecessary words and phrases.

## Setup

---

- Clone the repository
- Run the setup.py file to install the dependencies or `pip install -r requirements.txt`
- Navigate to `backend/config.py` file and adjust your settings. Examples for both database drivers have been provided in the file.
- Install a production asgi server of your choice. The 2 I recommend are [`hypercorn`](https://pypi.org/project/hypercorn/) and [`uvicorn`](https://pypi.org/project/uvicorn/).

## Running your ASGI server

---

#### Hypercorn

```sh
# inside the backend directory
hypercorn app:app --graceful-timeout 3 --workers 3
# outside of the backend directory
hypercorn backend.app:app --graceful-timeout 3 --workers 3
```

#### Uvicorn

```sh
# inside the backend directory
uvicorn app:app --workers 3
# outside of the backend directory
uvicorn backend.app:app --workers 3
```

Please keep in mind that both Uvicorn and Hypercorn support running applications through the Unix Domain Socket (UDS) protocol rather than the Transmission Control Protocol (TCP). The choice is yours.

On another note, keep in mind that the amount of workers you have will only affect performance if your machine's CPU core count supports it. Else, increasing the worker count will not be helpful at all.

⚠️ Minimum RAM needed for a single worker is around 2.5-3 Gbs. Please consider it and adjust worker according to your machine.

To read more about sockets and which protocol will be the right one for you, please refer to this article: https://www.digitalocean.com/community/tutorials/understanding-sockets

## Proxy

---

- In order to use API cleanly, I recommend placing yourself behind a proxy server. One of the most popular choices is [`NGINX`](https://www.nginx.com/).
- Examples for both the Nginx conf file and systemd service file are inside the examples folder.

## Get example (aiohttp)

---

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

###Loading a Chrome Extension in the Extension Folder

-Download the extension files and save them to a folder on your computer.
-Open the Google Chrome browser and navigate to the Extensions page. To do this, click on the three dots in the top right corner of the browser window and select "More tools" > "Extensions".
-Enable Developer mode by toggling the switch in the top right corner of the page.
-Click on the "Load unpacked" button in the top left corner of the page.
-In the file browser window, navigate to the folder where you saved the extension files and select the folder.
-Click "Open" to load the extension into Chrome.
-The extension should now be visible on the Extensions page, and you should see the extension icon in the top right corner of the browser window.
