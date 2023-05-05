import asyncio
import re
from constants import (
    CONNECTION_NOT_PRIVATE,
    SITE_NOT_REACHABLE,
    URL_KEYWORDS,
)
from playwright.async_api import async_playwright

URL_RX = re.compile(r"https?://(?:www\.)?.+")
SENTECE_RX = re.compile(r"^[A-Z][^?!]*(?:\.[^?!]*)*\.$", re.MULTILINE)
BASE_URL = "https://www.google.com/search?q="
TERMS_AND_CONDITIONS = "+terms+and+conditions"


async def scrape_website(browser, url: str) -> tuple | int:
    match_case = URL_RX.match(url)
    if match_case:
        page = await browser.new_page()
        await page.goto(url, wait_until="commit")
        text = await page.evaluate("document.body.innerText")
        text = re.findall(SENTECE_RX, text)
        text = "\n".join(text)
        if CONNECTION_NOT_PRIVATE in text:
            await page.close()
            return 500
        await page.close()
        return (text, False, url)
    else:
        return 500


async def scrape(browser, company: str) -> tuple | int:
    page = await browser.new_page()
    await page.goto(BASE_URL + company + TERMS_AND_CONDITIONS, wait_until="commit")
    text_of_link = await page.inner_text("xpath=//h3[@class='LC20lb MBeuO DKV0Md']")

    if any(keyword in text_of_link.lower() for keyword in URL_KEYWORDS):
        await page.click("xpath=//h3[@class='LC20lb MBeuO DKV0Md']")
        # get link of the site
        print("this working?")
        await page.wait_for_load_state("domcontentloaded")
        #  some javascript thing to get some information about the site
        print("working?")
        text = await page.evaluate("document.body.innerText")
        link = await page.evaluate("document.URL")
        # get all the sentences from the text
        text = re.findall(SENTECE_RX, text)
        text = "\n".join(text)

        if CONNECTION_NOT_PRIVATE in text or SITE_NOT_REACHABLE in text:
            await page.close()
            return 500
        await page.close()
        return (text, link)
    else:
        await page.close()
        return 500


if __name__ == "__main__":

    async def main():
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)        
        text = await scrape(browser, "docs")
        print(text)

    asyncio.run(main())
