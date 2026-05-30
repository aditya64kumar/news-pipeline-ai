import psycopg2
from config import DB_CONFIG

def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            source TEXT,
            published_at TIMESTAMP,
            url TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Table ready hai!")

if __name__ == "__main__":
    create_table()