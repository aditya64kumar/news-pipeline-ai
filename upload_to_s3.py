import boto3
import json
import psycopg2
from datetime import datetime
from config import DB_CONFIG
import os
from dotenv import load_dotenv

load_dotenv()

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

def fetch_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, description, source, 
               published_at, url, created_at 
        FROM news_articles
        ORDER BY created_at DESC
    """)
    
    rows = cursor.fetchall()
    articles = []
    
    for row in rows:
        articles.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "source": row[3],
            "published_at": str(row[4]),
            "url": row[5],
            "created_at": str(row[6])
        })
    
    cursor.close()
    conn.close()
    print(f"✅ {len(articles)} articles DB se mile!")
    return articles

def upload_to_s3(articles):
    s3 = get_s3_client()
    bucket = os.getenv('AWS_BUCKET_NAME')
    
    # Aaj ki date se folder structure
    today = datetime.now().strftime("%Y/%m/%d")
    filename = f"news/{today}/articles.json"
    
    # JSON format mein convert karo
    data = json.dumps(articles, ensure_ascii=False, indent=2)
    
    s3.put_object(
        Bucket=bucket,
        Key=filename,
        Body=data,
        ContentType='application/json'
    )
    
    print(f"✅ S3 pe upload ho gaya!")
    print(f"📁 Location: s3://{bucket}/{filename}")

if __name__ == "__main__":
    print("🚀 S3 Upload shuru ho raha hai...")
    articles = fetch_from_db()
    upload_to_s3(articles)
    print("✅ Complete!")