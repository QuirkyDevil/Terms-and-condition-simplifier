from backend.scrappers.selenium_based import scrap_text
from backend.models.sentence_classifier import classify_sentiment
from backend.models.summerizer import final_summary
from backend.functions.helper import preprocess


async def scrape_and_summarize(analyzer, url: str, points: int = 20):
    """This is the main function that will scrape the terms and conditions
    from the specified url and summarize them. First it will scrape the
    terms and conditions, then it will preprocess the text, then it will
    classify the sentences as positive or negative, returning only the
    negative sentences, and then it will summarize the negative sentences.
    It takes in the analyzer object, the url, and the number of maximum
    sentences to be in the summary. Default is 20.
    """
    text = await scrap_text(url)
    text = await preprocess(text)
    negative_text = await classify_sentiment(text, analyzer=analyzer)
    summary = await final_summary(negative_text, points)
    return summary


async def summerize_without_classify(url: str, points: int = 20):
    """This is similar function to the scrape_and_summarize function,
    except this will not classify the sentences as positive or negative.
    This is useful if you want to summarize the entire text, not just
    the negative sentences. The maximum number of sentences in the summary
    is 20 by default. You can change this by passing in the points argument.
    """
    text = await scrap_text(url)
    summary = await final_summary(text, points)
    return summary


async def summerize_usertext(analyzer, text: str, points: int = 20):
    """This is a function that will directly take user inputed terms and conditions and summerize it"""
    text = await preprocess(text)
    negative_text = await classify_sentiment(text, analyzer=analyzer)
    summary = await final_summary(negative_text, points)
    return summary
