import asyncio


from backend.scrappers.playwright_scrapper import scrape_website, scrape


async def main():
    try:
        await scrape("google")
        print("Done")
    except Exception as e:
        print(e)
        return 500
