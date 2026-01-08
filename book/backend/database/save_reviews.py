from datetime import datetime
from pymongo.errors import BulkWriteError
from database.mongo_connection import reviews_collection

def save_reviews(reviews, product_url):
    documents = []

    for r in reviews:
        doc = {
            "product_url": product_url,
            "review_text": r["review"],
            "rating": r.get("rating"),
            "sentiment": r["sentiment"],
            "compound_score": r["sentiment_score"],
            "source": "Snapdeal",
            "scraped_at": datetime.utcnow()
        }
        documents.append(doc)

    if not documents:
        return

    try:
        reviews_collection.insert_many(documents, ordered=False)
        print(f"✅ {len(documents)} new reviews saved")

    except BulkWriteError as e:
        inserted = len(documents) - len(e.details["writeErrors"])
        print(f"⚠️ {inserted} new reviews saved (duplicates skipped)")
