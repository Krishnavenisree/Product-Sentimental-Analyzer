import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import sys
import os
from contextlib import redirect_stdout, redirect_stderr


# ------------------ SILENT VADER CHECK ------------------
def ensure_vader():
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        # Suppress nltk download output
        with open(os.devnull, "w") as f:
            with redirect_stdout(f), redirect_stderr(f):
                nltk.download("vader_lexicon", quiet=True)


ensure_vader()
# --------------------------------------------------------


analyzer = SentimentIntensityAnalyzer()


def clean_text(text: str) -> str:
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.lower().strip()


def analyze_sentiment(review: str):
    cleaned = clean_text(review)
    scores = analyzer.polarity_scores(cleaned)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, compound
