import psycopg2
import os
from dotenv import load_dotenv
from config import DB_CONFIG

load_dotenv()

def migrate():
    print("🚀 Migration shuru ho rahi hai...")
    
    # Local DB se data lo
    local_conn = psycopg2.connect(**DB_CONFIG)
    local_cursor = local_conn.cursor()
    
    local_cursor.execute("""
        SELECT title, description, source, 
               published_at, url, ai_summary, sentiment
        FROM news_articles
        WHERE title IS NOT NULL
    """)
    rows = local_cursor.fetchall()
    print(f"✅ Local DB se {len(rows)} articles mile!")
    
    # Neon DB mein save karo
    neon_conn = psycopg2.connect(os.getenv('NEON_DB_URL'))
    neon_cursor = neon_conn.cursor()
    
    saved = 0
    for row in rows:
        try:
            neon_cursor.execute("""
                INSERT INTO news_articles 
                (title, description, source, published_at, url, ai_summary, sentiment)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            """, row)
            saved += 1
        except Exception as e:
            print(f"❌ Error: {e}")
    
    neon_conn.commit()
    
    local_cursor.close()
    local_conn.close()
    neon_cursor.close()
    neon_conn.close()
    
    print(f"✅ {saved} articles Neon pe migrate ho gaye!")

if __name__ == "__main__":
    migrate()