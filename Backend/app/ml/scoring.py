from app.utils.db import supabase

def score_company(ticker):
    # Get company id
    company = supabase.table("companies").select("*").eq("ticker", ticker).execute().data
    if not company:
        raise ValueError(f"No company found for ticker {ticker}")
    company_id = company[0]["id"]
    # Get latest financials
    financials = supabase.table("financials").select("*").eq("company_id", company_id).order("date", desc=True).limit(1).execute().data
    financials = financials[0] if financials else {}
    # Get recent news
    news_items = supabase.table("news").select("*").eq("company_id", company_id).order("date", desc=True).limit(5).execute().data
    # Compute score
    return compute_credit_score(financials, news_items)

def log_score(company_id, score, explanation):
    from datetime import datetime
    supabase.table("scores").insert({
        "company_id": company_id,
        "date": datetime.utcnow().isoformat(),
        "score": score,
        "explanation": explanation["plain_summary"],
    }).execute()


def compute_credit_score(financials, news_items):
    score = 50
    
    if financials.get("net_income") and financials.get("net_income") > 0:
        score += 20
    if financials.get("debt_ratio") and financials.get("debt_ratio") < 0.5:
        score += 20
    if financials.get("revenue") and financials.get("revenue") > 1_000_000_000:
        score += 10
    
    for n in news_items:
        if n.get("sentiment") == "negative":
            score -= 10
        elif n.get("sentiment") == "positive":
            score += 5

    score = min(100, max(0, score))
    return score
