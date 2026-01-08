from collections import Counter
import re
from nlp.sentiment_analyser import analyze_sentiment


def word_frequency(reviews):
    words = []
    for review in reviews:
        clean = re.sub(r"[^a-zA-Z ]", "", review.lower())
        words.extend(clean.split())
    return Counter(words).most_common(10)


def sentiment_distribution(sentiments):
    return {
        "Positive": sentiments.count("Positive"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral"),
    }


def analyze_reviews(reviews):
    sentiments = []

    for review in reviews:
        text = review.get("review", "")

        sentiment, score = analyze_sentiment(text)

        review["sentiment"] = sentiment
        review["sentiment_score"] = score

        sentiments.append(sentiment)

    analytics = {
        "sentiment_distribution": sentiment_distribution(sentiments),
        "top_words": word_frequency([r["review"] for r in reviews])
    }

    return reviews, analytics
