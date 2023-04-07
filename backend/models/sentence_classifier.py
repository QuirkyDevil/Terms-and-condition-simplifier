import re


async def classify_sentiment(para, analyzer) -> list:
    negative_list = []
    paragraph = re.split(r' *[\.\?!][\'"\)\]]* *', para)
    for text in paragraph:
        scores = analyzer.polarity_scores(text)
        if scores["compound"] <= -0.05:
            negative_list.append(text + ".")
    negative_string = " ".join(negative_list)
    return negative_string
