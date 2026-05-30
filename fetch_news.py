import requests
import feedparser
from config import NEWS_API_KEY, NEWS_URL

# RSS Feeds list
RSS_FEEDS = {
    "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "india": "https://timesofindia.indiatimes.com/rssfeeds/1221656.cms",
    "world": "http://feeds.bbci.co.uk/news/world/rss.xml"
}

def fetch_news_api(topic="technology"):
    params = {
        "q": topic,
        "language": "en",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print(f"✅ NewsAPI: {len(articles)} articles mile!")
        return articles
    else:
        print(f"❌ NewsAPI Error: {response.status_code}")
        return []

def fetch_rss(topic="technology"):
    url = RSS_FEEDS.get(topic)
    if not url:
        return []
    
    feed = feedparser.parse(url)
    articles = []
    
    for entry in feed.entries:
        articles.append({
            "title": entry.get("title"),
            "description": entry.get("summary"),
            "source": {"name": feed.feed.get("title", topic)},
            "publishedAt": entry.get("published"),
            "url": entry.get("link")
        })
    
    print(f"✅ RSS: {len(articles)} articles mile - {topic}!")
    return articles

def fetch_news(topic="technology"):
    # Dono se data lo
    api_articles = fetch_news_api(topic)
    rss_articles = fetch_rss(topic)
    return api_articles + rss_articles

if __name__ == "__main__":
    articles = fetch_news("technology")
    for article in articles:
        print(f"📰 {article['title']}")