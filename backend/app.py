from flask import Flask, request, jsonify
from database import SessionLocal, engine
from models import Base, News
import feedparser
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(bind=engine)

# Initialize NLP classifier
classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Fetch News
@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    session = SessionLocal()
    rss_feed = "https://example.com/rss"
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        news_item = News(
            title=entry.title,
            description=entry.summary,
            url=entry.link,
            category=categorize_news(entry.title + " " + entry.summary),
            source=entry.source.title
        )
        session.add(news_item)
    session.commit()
    session.close()
    return jsonify({"message": "News fetched and stored successfully."})

# Categorize News
def categorize_news(text):
    labels = ['Politics', 'Sports', 'Business', 'Technology', 'Entertainment']
    return classifier(text, labels)['labels'][0]

if __name__ == '__main__':
    app.run(debug=True)
