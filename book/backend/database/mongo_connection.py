from pymongo import MongoClient

MONGO_URI = "mongodb+srv://database1:12345@productsentimentdb.umpcvcj.mongodb.net/?appName=ProductSentimentDB"

client = MongoClient(MONGO_URI)

db = client["sentiment_analysis"]
reviews_collection = db["reviews"]
