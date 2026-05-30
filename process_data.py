import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

print("Script shuru ho rahi hai...")
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, length
import psycopg2
from config import DB_CONFIG
print("Script shuru ho rahi hai...")
def create_spark_session():
    spark = SparkSession.builder \
        .appName("NewsPipeline") \
        .config("spark.ui.showConsoleProgress", "false") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("OFF") 
    return spark

def fetch_data_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, description, source, 
               published_at, url 
        FROM news_articles
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def process_data():
    print("🚀 PySpark Processing Shuru...")
    
    spark = create_spark_session()
    
    # DB se data lo
    rows = fetch_data_from_db()
    print(f"✅ {len(rows)} articles DB se mile!")
    
    # Spark DataFrame banao
    columns = ["id", "title", "description", 
               "source", "published_at", "url"]
    df = spark.createDataFrame(rows, columns)
    
    print(f"📊 Total articles: {df.count()}")
    
    # Clean karo
    df_clean = df \
        .filter(col("title").isNotNull()) \
        .filter(length(col("title")) > 10) \
        .withColumn("title", trim(col("title"))) \
        .withColumn("source", trim(col("source"))) \
        .dropDuplicates(["url"])
    
    print(f"✅ Clean articles: {df_clean.count()}")
    
    # Source wise count
    print("\n📈 Source wise articles:")
    df_clean.groupBy("source") \
        .count() \
        .orderBy("count", ascending=False) \
        .show(10, truncate=False)
    
    spark.stop()
    print("✅ Processing Complete!")

if __name__ == "__main__":
    process_data()