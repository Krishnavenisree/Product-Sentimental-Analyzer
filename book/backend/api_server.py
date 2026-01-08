from flask import Flask, request, jsonify
from flask_cors import CORS

from scraper.scraper import scrape_all_books, save_to_csv

app = Flask(__name__)
CORS(app)

# Store scraped books in memory
scraped_books = []


@app.route("/", methods=["GET"])
def home():
    return {"status": "Backend API running successfully"}


# 🔹 Trigger scraping books from books.toscrape.com
@app.route("/scrape", methods=["POST"])
def scrape_books():
    global scraped_books
    
    data = request.get_json() or {}
    start_url = data.get("start_url", "http://books.toscrape.com/")

    scraped_books = scrape_all_books(start_url)
    
    # Save to CSV
    save_to_csv(scraped_books, "books_toscrape.csv")

    # Calculate rating distribution
    rating_distribution = {}
    for book in scraped_books:
        rating = book.get("rating")
        if rating:
            rating_distribution[rating] = rating_distribution.get(rating, 0) + 1

    return {
        "message": "Scraping completed",
        "total_books": len(scraped_books),
        "rating_distribution": rating_distribution
    }


# 🔹 Fetch scraped books
@app.route("/books", methods=["GET"])
def get_books():
    global scraped_books
    
    # Optional filtering by rating
    rating = request.args.get("rating", type=int)
    
    if rating:
        filtered = [b for b in scraped_books if b.get("rating") == rating]
        return jsonify(filtered)
    
    return jsonify(scraped_books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
