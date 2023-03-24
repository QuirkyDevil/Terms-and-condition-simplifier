# from textblob import TextBlob
#!pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# This code performs sentiment analysis on a given string by using the VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis tool. The string is split into paragraphs using regular expressions, and each paragraph is analyzed for sentiment using the VADER analyzer. The sentiment score of each paragraph is then printed to the console.

str1 = "We don't sell your personal data to advertisers, and we don't share information that directly identifies you (such as your name, email address or other contact information) with advertisers unless you give us specific permission. Instead, advertisers can tell us things such as the kind of audience that they want to see their ads, and we show those ads to people who may be interested. We provide advertisers with reports about the performance of their ads that help them understand how people are interacting with their content. See Section 2 below to learn more about how personalised advertising under these Terms works on the Meta Products."

paragraphs = re.split(r"\n\n+", str1)

print(paragraphs)

analyzer = SentimentIntensityAnalyzer()

for i, paragraphs in enumerate(paragraphs):
    # blob = TextBlob(paragraphs)
    # sentiment_score = blob.sentiment.polarity
    scores = analyzer.polarity_scores(paragraphs)
    # print(paragraphs[i])
    # print(sentiment_score)
    print(scores["compound"])
