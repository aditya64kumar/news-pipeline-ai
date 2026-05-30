import psycopg2
from config import DB_CONFIG

def store_articles(articles):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    saved = 0
    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO news_articles 
                (title, description, source, published_at, url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            """, (
                article.get("title"),
                article.get("description"),
                article.get("source", {}).get("name"),
                article.get("publishedAt"),
                article.get("url")
            ))
            saved += 1
        except Exception as e:
            print(f"❌ Error: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {saved} articles database mein save ho gaye!")

if __name__ == "__main__":
    from fetch_news import fetch_news
    articles = fetch_news("technology")
    store_articles(articles)