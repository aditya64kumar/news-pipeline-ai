from fetch_news import fetch_news
from store_news import store_articles
from upload_to_s3 import fetch_from_db, upload_to_s3

def run_pipeline():
    print("🚀 Pipeline shuru ho rahi hai...")
    
    topics = ["technology", "business", "science", "india", "world"]
    
    for topic in topics:
        print(f"\n📡 Topic: {topic}")
        articles = fetch_news(topic)
        store_articles(articles)
    
    # S3 pe upload karo
    print("\n☁️ S3 pe upload ho raha hai...")
    articles = fetch_from_db()
    upload_to_s3(articles)
    
    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()