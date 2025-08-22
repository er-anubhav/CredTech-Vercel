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
    score = 50  # Neutral baseline
    explanation = []
    feature_contributions = {}

    # --- Financial Factors (70% weight) ---
    net_income = financials.get("net_income", 0) or 0
    revenue = financials.get("revenue", 0) or 0
    debt_ratio = financials.get("debt_ratio", None)

    # Net income (profitability) - up to +20 / -15
    if net_income > 0:
        bonus = min(20, (net_income / 1_000_000_000) * 10)
        score += bonus
        feature_contributions["net_income"] = bonus
        explanation.append(f"✅ Positive net income → +{bonus:.1f}")
    else:
        score -= 15
        feature_contributions["net_income"] = -15
        explanation.append("❌ Negative net income → -15")

    # Revenue scale - up to +15
    if revenue > 10_000_000_000:
        score += 15
        feature_contributions["revenue"] = 15
        explanation.append("✅ Very high revenue (>10B) → +15")
    elif revenue > 1_000_000_000:
        score += 10
        feature_contributions["revenue"] = 10
        explanation.append("✅ Strong revenue (>1B) → +10")
    elif revenue > 100_000_000:
        score += 5
        feature_contributions["revenue"] = 5
        explanation.append("✅ Moderate revenue (>100M) → +5")
    else:
        feature_contributions["revenue"] = 0
        explanation.append("ℹ️ Low revenue (<100M) → +0")

    # Debt ratio - up to +15 or -20
    if debt_ratio is not None:
        if debt_ratio < 0.3:
            score += 15
            feature_contributions["debt_ratio"] = 15
            explanation.append("✅ Low debt ratio (<0.3) → +15")
        elif debt_ratio < 0.5:
            score += 10
            feature_contributions["debt_ratio"] = 10
            explanation.append("✅ Moderate debt ratio (<0.5) → +10")
        elif debt_ratio < 0.7:
            score -= 5
            feature_contributions["debt_ratio"] = -5
            explanation.append("⚠️ High debt ratio (<0.7) → -5")
        else:
            score -= 20
            feature_contributions["debt_ratio"] = -20
            explanation.append("❌ Very high debt ratio (≥0.7) → -20")
    else:
        feature_contributions["debt_ratio"] = 0
        explanation.append("ℹ️ No debt ratio data → +0")

    # --- News Sentiment (30% weight) ---
    pos_count = sum(1 for n in news_items if n.get("sentiment") == "positive")
    neg_count = sum(1 for n in news_items if n.get("sentiment") == "negative")

    if pos_count:
        bonus = min(20, pos_count * 5)
        score += bonus
        feature_contributions["positive_news"] = bonus
        explanation.append(f"✅ {pos_count} positive news → +{bonus}")
    else:
        feature_contributions["positive_news"] = 0
        explanation.append("ℹ️ No positive news → +0")

    if neg_count:
        penalty = min(25, neg_count * 8)
        score -= penalty
        feature_contributions["negative_news"] = -penalty
        explanation.append(f"⚠️ {neg_count} negative news → -{penalty}")
    else:
        feature_contributions["negative_news"] = 0
        explanation.append("✅ No negative news → +0")

    # --- Clamp score ---
    score = min(100, max(0, round(score)))

    return score
