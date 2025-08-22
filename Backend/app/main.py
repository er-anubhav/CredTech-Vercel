from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils.db import supabase

from app.ml.explainability import explain_score
from app.ml.scoring import score_company, compute_credit_score
from app.api.companies import router as companies_router



app = FastAPI()
app.include_router(companies_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Only allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/companies")
def get_companies():
    companies = supabase.table("companies").select("*").execute().data
    return companies

@app.get("/company/{ticker}")
def get_company(ticker: str):
    data = supabase.table("companies").select("*").eq("ticker", ticker).execute().data
    if not data:
        raise HTTPException(status_code=404, detail="Company not found")
    return data[0]


@app.get("/news/{ticker}")
def get_news(ticker: str):
    data = supabase.table("companies").select("*").eq("ticker", ticker).execute().data
    if not data or len(data) == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    company_id = data[0]["id"]
    news = supabase.table("news").select("*").eq("company_id", company_id).order("date", desc=True).limit(5).execute().data
    return news


@app.get("/score/{ticker}")
def get_score(ticker: str):
    try:
        # --- Fetch company and data ---
        company = supabase.table("companies").select("*").eq("ticker", ticker).execute().data
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        company_id = company[0]["id"]
        financials_list = supabase.table("financials").select("*").eq("company_id", company_id).order("date", desc=True).limit(1).execute().data
        if not financials_list or not isinstance(financials_list, list) or len(financials_list) == 0:
            raise HTTPException(status_code=404, detail="Financials not found for this company")
        financials = financials_list[0]
        news_items = supabase.table("news").select("*").eq("company_id", company_id).order("date", desc=True).limit(5).execute().data or []

        # --- Compute score ---
        score = compute_credit_score(financials, news_items)

        # --- Generate explainability breakdown ---
        explanation = explain_score(financials, news_items, score)  # returns dict

        return {
            "ticker": ticker,
            "score": score,
            "explanation": explanation["plain_summary"],
            "feature_contributions": explanation["feature_contributions"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/score_history/{ticker}")
def get_score_history(ticker: str):
    company = supabase.table("companies").select("*").eq("ticker", ticker).execute().data
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    company_id = company[0]["id"]
    scores = (
        supabase.table("scores")
        .select("date,score,explanation")
        .eq("company_id", company_id)
        .order("date", desc=False)
        .execute()
        .data
    )
    return scores
