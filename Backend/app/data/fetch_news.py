import requests
import logging
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY, NEWS_API_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_and_store_news(company_name, company_id):
    logging.info(f"Fetching news for {company_name} (company_id={company_id})")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "sortBy": "publishedAt",
        "pageSize": 5,  # Latest 5 headlines
        "apiKey": NEWS_API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        logging.error(f"News API error {resp.status_code} for {company_name}")
        return

    news_items = resp.json().get("articles", [])
    logging.info(f"Fetched {len(news_items)} news articles for {company_name}")
    for article in news_items:
        title = article["title"]
        news_url = article["url"]
        published_at = article["publishedAt"]

        sentiment = ("negative" if any(x in title.lower() for x in ["loss", "down", "lawsuit", "fraud", "resign"])
                     else "positive" if any(x in title.lower() for x in ["profit", "up", "record", "raises", "growth"])
                     else "neutral")

        logging.info(f"Inserting news: '{title[:60]}...' for company_id={company_id} with sentiment={sentiment}")
        supabase.table("news").insert({
            "company_id": company_id,
            "title": title,
            "url": news_url,
            "date": published_at,
            "sentiment": sentiment,
        }).execute()
    logging.info(f"Completed storing news for {company_name}")
