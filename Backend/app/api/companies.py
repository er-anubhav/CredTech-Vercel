
from fastapi import APIRouter, HTTPException
from app.utils.db import supabase
import yfinance as yf
import time
from app.data.fetch_financials import save_company_and_financials
from app.ml.scoring import score_company, log_score
from app.ml.explainability import explain_score

router = APIRouter()


@router.post("/add_company/{ticker}")
def add_company_by_ticker(ticker: str):
	ticker = ticker.upper()
	# Check if company already exists
	existing = supabase.table("companies").select("id").eq("ticker", ticker).execute().data
	if existing:
		return {"message": "Company already exists", "id": existing[0]["id"]}
	# Fetch and store company, financials, news
	save_company_and_financials(ticker)

	# Retry logic for eventual consistency
	def retry_fetch(fetch_fn, max_retries=5, base_delay=0.3):
		delay = base_delay
		for attempt in range(max_retries):
			result = fetch_fn()
			if result:
				return result
			time.sleep(delay)
			delay *= 2
		return None

	# Get company id with retry
	company = retry_fetch(lambda: supabase.table("companies").select("id").eq("ticker", ticker).execute().data)
	if not company:
		raise HTTPException(status_code=500, detail="Company insert failed (timing issue)")
	company_id = company[0]["id"]
	# Get latest financials with retry
	financials = retry_fetch(lambda: supabase.table("financials").select("*").eq("company_id", company_id).order("date", desc=True).limit(1).execute().data)
	financials = financials[0] if financials else {}
	# Get recent news with retry
	news_items = retry_fetch(lambda: supabase.table("news").select("*").eq("company_id", company_id).order("date", desc=True).limit(5).execute().data)
	news_items = news_items if news_items else []
	# Compute score
	score = score_company(ticker)
	# Explain score
	explanation = explain_score(financials, news_items, score)
	# Log score
	log_score(company_id, score, explanation)
	return {
		"message": "Company created and scored",
		"id": company_id,
		"score": score,
		"explanation": explanation["plain_summary"],
		"feature_contributions": explanation["feature_contributions"]
	}

@router.post("/company")
def upsert_company(company: dict):
	ticker = company.get("ticker")
	if not ticker:
		raise HTTPException(status_code=400, detail="Ticker is required")
	# Check if company exists
	existing = supabase.table("companies").select("id").eq("ticker", ticker).execute().data
	if existing:
		# Update existing
		company_id = existing[0]["id"]
		supabase.table("companies").update(company).eq("id", company_id).execute()
		return {"message": "Company updated", "id": company_id}
	else:
		# Insert new
		res = supabase.table("companies").insert(company).execute()
		return {"message": "Company created", "id": res.data[0]["id"]}
