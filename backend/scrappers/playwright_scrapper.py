import asyncio
import re
from backend.scrappers.constants import (
    CONNECTION_NOT_PRIVATE,
    SITE_NOT_REACHABLE,
    URL_KEYWORDS,
)
from playwright.async_api import async_playwright

URL_RX = re.compile(r"https?://(?:www\.)?.+")
SENTECE_RX = re.compile(r"^[A-Z][^?!]*(?:\.[^?!]*)*\.$", re.MULTILINE)
BASE_URL = "https://www.google.com/search?q="
TERMS_AND_CONDITIONS = "+terms+and+conditions"


def is_valid_url(url: str) -> bool:
    """Check if the url is valid or not"""
    match_case = URL_RX.match(url)
    return bool(match_case)


async def scrape_website(browser, url: str) -> tuple | int:
    """Scrape the website from url and return the text of the website"""
    if is_valid_url(url):
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="commit")
            text = await page.evaluate("document.body.innerText")
            text = re.findall(SENTECE_RX, text)
            text = "\n".join(text)
            if CONNECTION_NOT_PRIVATE or SITE_NOT_REACHABLE in text:
                await page.close()
                return 500
            await page.close()
            return (text, False, url)
        except Exception:
            await page.close()
            return 500
    else:
        return 500


async def scrape(browser, company: str) -> tuple | int:
    """Scrape the website and return the text of the website"""
    page = await browser.new_page()

    # Try to navigate to the company's terms and conditions page
    try:
        await page.goto(BASE_URL + company + TERMS_AND_CONDITIONS, wait_until="commit")
    except Exception:
        await page.close()
        return 500

    # Get the text of the link
    text_of_link = await page.inner_text("xpath=//h3[@class='LC20lb MBeuO DKV0Md']")

    # Check if the text of the link matches any of the keywords
    if any(keyword in text_of_link.lower() for keyword in URL_KEYWORDS):
        try:
            # Click on the link and wait for the page to load
            await page.click("xpath=//h3[@class='LC20lb MBeuO DKV0Md']")
            await page.wait_for_load_state("domcontentloaded")

            # Get the text and link of the page
            text = await page.evaluate("document.body.innerText")
            link = await page.evaluate("document.URL")
        except Exception:
            await page.close()
            return 500

        # Get only the sentences from the text
        text = re.findall(SENTECE_RX, text)
        text = "\n".join(text)

        # Check if the connection is not private or the site is not reachable
        if CONNECTION_NOT_PRIVATE or SITE_NOT_REACHABLE in text:
            await page.close()
            return 500

        # Close the page
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
