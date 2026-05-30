import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import psycopg2
from config import DB_CONFIG
from dotenv import load_dotenv

load_dotenv()

# Gemini Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# Prompt Template
prompt = PromptTemplate(
    input_variables=["title", "description"],
    template="""
    News Article:
    Title: {title}
    Description: {description}
    
    Please provide:
    1. Summary: (2 lines mein summary)
    2. Sentiment: (Positive/Negative/Neutral)
    
    Format:
    SUMMARY: <summary here>
    SENTIMENT: <sentiment here>
    """
)

chain = prompt | llm

def analyze_article(title, description):
    try:
        result = chain.invoke({
            "title": title,
            "description": description or "No description available"
        })
        return result.content
    except Exception as e:
        return f"Error: {e}"

def process_articles():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Sirf jo articles process nahi hue
    cursor.execute("""
        SELECT id, title, description 
        FROM news_articles 
        WHERE title IS NOT NULL
        AND ai_summary IS NULL
        LIMIT 50
    """)
    
    articles = cursor.fetchall()
    print(f"✅ {len(articles)} articles mile!\n")
    
    for article in articles:
        id, title, description = article
        print(f"📰 {title[:60]}...")
        
        result = analyze_article(title, description)
        
        # Result parse karo
        summary = ""
        sentiment = ""
        
        for line in result.split('\n'):
            if line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()
            if line.startswith("SENTIMENT:"):
                sentiment = line.replace("SENTIMENT:", "").strip()
        
        # DB mein save karo
        cursor.execute("""
            UPDATE news_articles 
            SET ai_summary = %s, sentiment = %s
            WHERE id = %s
        """, (summary, sentiment, id))
        conn.commit()
        
        print(f"📝 Summary: {summary[:80]}...")
        print(f"😊 Sentiment: {sentiment}")
        print("-" * 50)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("🤖 AI Summarizer Shuru Ho Raha Hai...\n")
    process_articles()
    print("\n✅ Complete!")