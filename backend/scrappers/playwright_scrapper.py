import asyncio
from playwright.async_api import async_playwright
import re
from backend.scrappers.constants import *

URL_RX = re.compile(r"https?://(?:www\.)?.+")
SENTECE_RX = re.compile(r"^[A-Z][^?!]*(?:\.[^?!]*)*\.$", re.MULTILINE)
print("testing")


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


async def scrape(company: str) -> tuple | int:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        is_same_company = False
        page = await browser.new_page()
        await page.goto(
            "https://www.google.com/search?q=" + company + "+terms+and+conditions",
            wait_until="commit",
        )
        text_of_link = await page.inner_text("xpath=//h3[@class='LC20lb MBeuO DKV0Md']")
        link = await page.inner_text("xpath=//cite[contains(@class, 'qLRx3b')]")

        company_regex = re.compile(r"\b{}\b".format(re.escape(company)), re.IGNORECASE)
        if company_regex.search(link):
            is_same_company = True

        if any(keyword in text_of_link.lower() for keyword in URL_KEYWORDS):
            await page.click("xpath=//h3[@class='LC20lb MBeuO DKV0Md']")
            # wait untill body loads
            await page.wait_for_selector("xpath=//body")
            text = await page.evaluate("document.body.innerText")
            # filter the text so remove if there is no full stop
            text = re.findall(SENTECE_RX, text)
            text = "\n".join(text)
            if CONNECTION_NOT_PRIVATE in text or SITE_NOT_REACHABLE in text:
                await page.close()
                return 500
            await page.close()
            return text
        else:
            await page.close()
            return 500


if __name__ == "__main__":

    async def main():
        text = await scrape("alibaba")
        print(text)

    asyncio.run(main())
