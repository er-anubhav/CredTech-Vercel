import yfinance as yf
import logging
import pandas as pd
from supabase import create_client, Client
import os
from .fetch_news import fetch_and_store_news
from app.config import SUPABASE_URL, SUPABASE_KEY, NEWS_API_KEY

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_company_and_financials(ticker):
    logging.info(f"Fetching financial data for {ticker}")
    stock = yf.Ticker(ticker)
    info = stock.info
    logging.info(f"Fetched info for {ticker}")
    financials = stock.financials
    logging.info(f"Fetched financials for {ticker}")

    name = info.get("shortName", "")
    sector = info.get("sector", "")

    logging.info(f"Upserting company {ticker} into database")
    company = supabase.table("companies").upsert({
        "ticker": ticker,
        "name": name,
        "sector": sector
    }).execute().data[0]
    company_id = company["id"]
    logging.info(f"Company upserted with id {company_id}")

    years = pd.to_datetime(financials.columns, errors='coerce').year
    logging.info(f"Extracted years from financials columns: {years.tolist()}")
    year = str(years[0]) if len(years) > 0 else "Unknown"
    try:
        net_income = float(financials.loc["Net Income"].iloc[0])
        logging.info(f"Net income: {net_income}")
    except Exception as e:
        logging.warning(f"Failed to get net income: {e}")
        net_income = None
    try:
        revenue = float(financials.loc["Total Revenue"].iloc[0])
        logging.info(f"Revenue: {revenue}")
    except Exception as e:
        logging.warning(f"Failed to get revenue: {e}")
        revenue = None
    debt_ratio = None

    logging.info(f"Inserting financials for {ticker} year {year}")
    supabase.table("financials").insert({
        "company_id": company_id,
        "date": f"{year}-01-01" if year != "Unknown" else None,
        "net_income": float(net_income) if net_income else None,
        "revenue": float(revenue) if revenue else None,
        "debt_ratio": float(debt_ratio) if debt_ratio else None,
    }).execute()
    logging.info(f"Inserted financials for {ticker} year {year}")
    fetch_and_store_news(name, company_id)
