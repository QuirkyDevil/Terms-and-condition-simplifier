import re

from backend.scrappers.selenium_based import scrap_text
from backend.models.sentence_classifier import classify_sentiment
from backend.models.summerizer import final_summary


async def preprocess(text):
    """This function preprocesses the text by removing html tags, new lines, tabs and extra spaces"""
    text = text.encode("ascii", "ignore").decode()  # remove non-ascii characters
    text = re.sub(r"<.*?>", "", text)  # remove html tags
    text = re.sub(r"[\n\t]+", " ", text)  # remove new lines and tabs
    text = re.sub(r" +", " ", text).strip()  # remove extra spaces
    return text


async def scrape_and_summarize(analyzer,  url: str, points: int = 20):
    """Scrape the terms and conditions and summarize them"""
    text = await scrap_text(url)
    text = await preprocess(text)
    negative_text = await classify_sentiment(text, analyzer=analyzer)
    summary = await final_summary(negative_text, points)
    return summary


async def summerize_without_classify(url: str, points: int = 20):
    """Scrape the terms and conditions and summarize them"""
    text = await scrap_text(url)
    summary = await final_summary(text, points)
    return summary

