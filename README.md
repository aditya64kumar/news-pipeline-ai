# 📰 News Intelligence Pipeline with AI

> End-to-end Data Engineering project — News fetch karo, AI se summarize karo, live dashboard pe dekho!

---

## 🏗️ Architecture

```
NewsAPI + RSS Feeds          # Data Sources
        ↓
   fetch_news.py             # News fetch karta hai
        ↓
  store_news.py              # Database mein save karta hai
        ↓
PostgreSQL ──→ Neon DB       # Local → Cloud DB
        ↓           ↓
upload_to_s3.py   dashboard.py   # S3 backup + Dashboard
        ↓                ↓
     AWS S3       Streamlit Cloud # Cloud Storage + Live UI
        ↓
  process_data.py            # PySpark se clean karo
        ↓
  ai_summarizer.py           # Gemini AI se summarize karo
        ↓
  Live Dashboard             # Sab kuch yahan dikhega!
```

---

## 🚀 Tech Stack

| Layer | Technology | Kaam |
|-------|-----------|------|
| **Data Ingestion** | NewsAPI, RSS Feeds | News fetch karna |
| **Database** | PostgreSQL, Neon DB | Data store karna |
| **Cloud Storage** | AWS S3 | Data lake backup |
| **Data Processing** | Apache PySpark | Big data clean karna |
| **AI Layer** | LangChain + Google Gemini | Summary + Sentiment |
| **Orchestration** | Windows Task Scheduler | Daily automation |
| **Dashboard** | Streamlit | Live visualization |
| **Language** | Python 3.12 | Sab kuch! |

---

## 📁 Project Structure

```
news_pipeline/
│
├── config.py            # Saari settings ek jagah (.env se load hoti hain)
├── fetch_news.py        # NewsAPI + RSS se news fetch karta hai
├── store_news.py        # Articles ko PostgreSQL/Neon mein save karta hai
├── db_setup.py          # Database aur tables banata hai
├── process_data.py      # PySpark se data clean + transform karta hai
├── ai_summarizer.py     # LangChain + Gemini se AI summary banata hai
├── upload_to_s3.py      # Data ko AWS S3 pe upload karta hai
├── migrate_to_neon.py   # Local DB se Neon Cloud pe migrate karta hai
├── dashboard.py         # Streamlit live dashboard
├── main.py              # Pura pipeline ek jagah se chalata hai
├── run_pipeline.bat     # Windows automation script
├── requirements.txt     # Saari Python libraries
└── .env                 # Secret keys (GitHub pe nahi jaata!)
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.12+
- Java 17 (PySpark ke liye zaroori)
- PostgreSQL 17
- AWS Account (Free Tier)
- Google AI Studio Account (Gemini API)
- NewsAPI Account (Free)

### 1. Clone the Repository

```bash
git clone https://github.com/aditya64kumar/news-pipeline-ai.git
cd news-pipeline-ai
```

### 2. Virtual Environment Banao

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Libraries Install Karo

```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup

`.env` file banao root folder mein:

```env
# NewsAPI Key — newsapi.org se lo
NEWS_API_KEY=your_newsapi_key

# Local PostgreSQL Settings
DB_HOST=localhost
DB_NAME=news_pipeline
DB_USER=postgres
DB_PASSWORD=your_password

# AWS S3 Settings — AWS Console se lo
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=ap-south-1

# Google Gemini API — aistudio.google.com se lo
GEMINI_API_KEY=your_gemini_api_key

# Neon Cloud DB — neon.tech se lo
NEON_DB_URL=your_neon_connection_string
```

### 5. Database Setup

```bash
# PostgreSQL mein table banao
python db_setup.py
```

---

## 🔄 Pipeline — Step by Step

### Step 1 — News Fetch Karo
```bash
python fetch_news.py
```
- NewsAPI se live news fetch karta hai
- BBC, Times of India RSS feeds se articles leta hai
- Topics: Technology, Business, Science, India, World

### Step 2 — Database Mein Save Karo
```bash
python store_news.py
```
- Articles PostgreSQL/Neon mein save karta hai
- Duplicate articles automatically skip hote hain (URL based)

### Step 3 — AWS S3 Pe Upload Karo
```bash
python upload_to_s3.py
```
- Data ko JSON format mein S3 pe save karta hai
- Date-wise folder structure:
```
s3://bucket/news/YYYY/MM/DD/articles.json
```

### Step 4 — PySpark Se Process Karo
```bash
python process_data.py
```
- Null values remove karta hai
- Duplicate articles clean karta hai
- Whitespace trim karta hai
- Source-wise analytics nikalta hai

### Step 5 — AI Summary Banao
```bash
python ai_summarizer.py
```
- Har article ka 2-line summary banata hai
- Sentiment detect karta hai (Positive/Negative/Neutral)
- Google Gemini AI use karta hai

### Step 6 — Pura Pipeline Ek Saath Chalao
```bash
python main.py
```
Sab steps automatically sequence mein chalte hain!

---

## 🤖 Automation

### Windows Task Scheduler
Pipeline rozana **12:15 AM** pe automatically chalti hai:
```
Task Scheduler → run_pipeline.bat → main.py → Complete!
```

Manually test karne ke liye:
```bash
.\run_pipeline.bat
```

---

## 📊 Live Dashboard

### Local Pe Chalao
```bash
streamlit run dashboard.py
```
Browser mein khulega: `http://localhost:8501`

### Live Cloud URL
```
https://news-pipeline-ai-7jmhaaxv5ml9whd7pusywn.streamlit.app
```

### Dashboard Features
- 📊 Total articles count
- 😊 Sentiment distribution chart (Positive/Negative/Neutral)
- 📈 Source-wise article bar chart
- 🔍 Filter by source and sentiment
- 📰 Article cards with AI summaries
- 🔗 Direct links to original articles

---

## ☁️ Cloud Architecture

```
# Daily Pipeline Flow:
Local Machine (12:15 AM)
        ↓ fetch + process
Neon DB (PostgreSQL Cloud)
        ↓ read data
Streamlit Cloud → Live Dashboard

# Backup Flow:
Local Machine
        ↓ upload JSON
AWS S3 (Data Lake)
```

---

## 📈 Sample Output

```
🚀 Pipeline shuru ho rahi hai...

📡 Topic: technology
✅ NewsAPI: 1 articles mile!
✅ RSS: 21 articles mile - technology!
✅ 22 articles Neon DB mein save ho gaye!

📡 Topic: business
✅ NewsAPI: 3 articles mile!
✅ RSS: 52 articles mile - business!
✅ 55 articles Neon DB mein save ho gaye!

📡 Topic: science
✅ RSS: 42 articles mile - science!
✅ 42 articles Neon DB mein save ho gaye!

☁️ S3 pe upload ho raha hai...
✅ S3 pe upload ho gaya!
📁 Location: s3://bucket/news/2026/05/30/articles.json

✅ Pipeline complete!
```

---

## 🎯 Key Features

- ✅ **Fully Automated** — Rozana bina kuch kiye pipeline chalti hai
- ✅ **AI Powered** — Google Gemini se smart summaries
- ✅ **Cloud Native** — AWS S3 + Neon DB + Streamlit Cloud
- ✅ **Scalable** — PySpark millions of records handle kar sakta hai
- ✅ **Duplicate Safe** — URL based deduplication
- ✅ **Multi Source** — NewsAPI + BBC + Times of India RSS
- ✅ **Live Dashboard** — Real-time data visualization

---

## 👨‍💻 Author

**Aditya Kumar**
- 🐙 GitHub: [@aditya64kumar](https://github.com/aditya64kumar)
- 💼 11 years Python Automation Experience
- 🎯 Transitioning to: Data Engineering + AI

---

## 📄 License

MIT License — freely use and modify!