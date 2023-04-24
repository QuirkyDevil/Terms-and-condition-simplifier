import re

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


async def classify_sentiment(para) -> list:
    """This function will classify the sentences as positive or negative.
    It will return a list of negative sentences. It takes in the paragraph
    and the analyzer object. The analyzer object is the object that will
    classify the sentences as positive or negative. It is created in the
    backend/functions/main.py file.
    """
    negative_list = []
    paragraph = re.split(r' *[\.\?!][\'"\)\]]* *', para)
    for text in paragraph:
        scores = analyzer.polarity_scores(text)
        if scores["compound"] <= -0.05:
            negative_list.append(text + ".")
    negative_string = " ".join(negative_list)
    return negative_string
