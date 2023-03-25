# How VaderSentiment Works
# VADER (Valence Aware Dictionary and sEntiment Reasoner) is a rule-based sentiment analysis tool that is specifically designed to analyze sentiment in social media. It uses a lexicon of words and phrases that are associated with positive or negative sentiment, as well as a set of rules for combining these words and phrases to calculate the sentiment of a text.

# The VADER lexicon contains over 7,500 words and phrases that are associated with positive or negative sentiment. Each word or phrase in the lexicon is assigned a sentiment score between -4 and 4, with negative scores indicating negative sentiment and positive scores indicating positive sentiment. The scores are also normalized to a range between -1 and 1 for easier interpretation.

# VADER uses a set of rules to combine the sentiment scores of the words and phrases in a text to calculate an overall sentiment score for the text. The rules take into account factors such as the presence of intensifiers and negators, as well as the context in which the words and phrases appear.

# Overall, VADER is a fast and effective tool for analyzing sentiment in social media and other forms of text. It is particularly useful for analyzing short, informal texts such as tweets and Facebook posts, where traditional machine learning approaches may not perform as well.

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

negative_tc = []


def analyze_sentiment(str1):
    paragraphs = re.split(r"\n\n+", str1)

    analyzer = SentimentIntensityAnalyzer()

    for i, paragraph in enumerate(paragraphs):
        scores = analyzer.polarity_scores(paragraph)

        if scores["compound"] < 0:
            negative_tc.append(paragraph)


str = """Our service provides a platform for people to connect with others and build communities. By using our platform, you agree to our terms and conditions.

We are committed to protecting your privacy and will never sell your personal data to advertisers or third parties without your consent. However, we may use your data to provide you with personalized ads based on your interests.

You acknowledge that our platform may be subject to downtime or interruptions, and we cannot guarantee that our service will always be available or error-free. You agree to hold us harmless for any damages or losses that may arise from your use of our platform.

By using our service, you agree to indemnify and hold us harmless from any claims, damages, or expenses arising from your violation of our terms and conditions. We reserve the right to terminate your access to our platform at any time, without notice, if we believe you have violated our terms.

We believe in fostering a positive and inclusive community, and we reserve the right to remove any content or users that we deem to be harmful, discriminatory, or in violation of our community guidelines. We encourage you to report any inappropriate behavior or content to us immediately.

By using our platform, you acknowledge and agree to our privacy policy, which explains how we collect, use, and disclose your personal data. If you have any questions or concerns about our terms and conditions or privacy policy, please contact us at support@ourplatform.com."""

analyze_sentiment(str)

print(negative_tc)
