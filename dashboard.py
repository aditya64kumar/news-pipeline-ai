import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from config import DB_CONFIG
import os
from dotenv import load_dotenv
load_dotenv()

# Page Config
st.set_page_config(
    page_title="News Intelligence Dashboard",
    page_icon="📰",
    layout="wide"
)

# DB se data load karo
@st.cache_data(ttl=300)
def load_data():
    conn = psycopg2.connect(os.getenv('NEON_DB_URL'))
    df = pd.read_sql("""
        SELECT 
            id, title, description, source,
            published_at, url, ai_summary, sentiment
        FROM news_articles
        WHERE title IS NOT NULL
        ORDER BY published_at DESC
    """, conn)
    conn.close()
    return df

# Dashboard
st.title("📰 News Intelligence Dashboard")
st.markdown("---")

# Data Load
df = load_data()

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Articles", len(df))
with col2:
    positive = len(df[df['sentiment'] == 'Positive'])
    st.metric("😊 Positive News", positive)
with col3:
    negative = len(df[df['sentiment'] == 'Negative'])
    st.metric("😟 Negative News", negative)
with col4:
    neutral = len(df[df['sentiment'] == 'Neutral'])
    st.metric("😐 Neutral News", neutral)

st.markdown("---")

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Source wise Articles")
    source_count = df['source'].value_counts().head(10).reset_index()
    source_count.columns = ['Source', 'Count']
    fig = px.bar(source_count, x='Count', y='Source', 
                 orientation='h', color='Count',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("😊 Sentiment Distribution")
    sentiment_count = df['sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['Sentiment', 'Count']
    colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
    fig = px.pie(sentiment_count, values='Count', names='Sentiment',
                 color='Sentiment', color_discrete_map=colors)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Filters
st.subheader("🔍 Articles Filter Karo")
col1, col2 = st.columns(2)

with col1:
    sources = ["All"] + list(df['source'].unique())
    selected_source = st.selectbox("Source Select Karo", sources)

with col2:
    sentiments = ["All", "Positive", "Negative", "Neutral"]
    selected_sentiment = st.selectbox("Sentiment Select Karo", sentiments)

# Filter Apply
filtered_df = df.copy()
if selected_source != "All":
    filtered_df = filtered_df[filtered_df['source'] == selected_source]
if selected_sentiment != "All":
    filtered_df = filtered_df[filtered_df['sentiment'] == selected_sentiment]

st.markdown(f"**{len(filtered_df)} articles found**")
st.markdown("---")

# Articles Display
for _, row in filtered_df.head(20).iterrows():
    with st.expander(f"📰 {row['title']}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Source:** {row['source']}")
            if row['ai_summary']:
                st.markdown(f"**AI Summary:** {row['ai_summary']}")
            else:
                st.markdown(f"**Description:** {row['description']}")
        with col2:
            sentiment = row['sentiment']
            if sentiment == 'Positive':
                st.success(f"😊 {sentiment}")
            elif sentiment == 'Negative':
                st.error(f"😟 {sentiment}")
            else:
                st.info(f"😐 {sentiment or 'Unknown'}")
            if row['url']:
                st.markdown(f"[🔗 Read More]({row['url']})")