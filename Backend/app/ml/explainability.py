def explain_score(financials, news_items, score):
    explanation_parts = []
    feature_contributions = {}

    # Net income
    if financials.get("net_income") and financials.get("net_income") > 0:
        feature_contributions["net_income"] = 20
        explanation_parts.append(f"Net Income is positive, added 20 to score.")
    else:
        feature_contributions["net_income"] = 0

    # Debt ratio
    if financials.get("debt_ratio") and financials.get("debt_ratio") < 0.5:
        feature_contributions["debt_ratio"] = 20
        explanation_parts.append("Debt ratio is low, added 20 to score.")
    elif financials.get("debt_ratio"):
        feature_contributions["debt_ratio"] = 0
        explanation_parts.append("Debt ratio is high, no bonus.")
    else:
        feature_contributions["debt_ratio"] = 0

    # Revenue
    if financials.get("revenue") and financials.get("revenue") > 1_000_000_000:
        feature_contributions["revenue"] = 10
        explanation_parts.append("Revenue is high, added 10 to score.")
    else:
        feature_contributions["revenue"] = 0

    # News-based
    pos_news = sum(1 for n in news_items if n.get("sentiment") == "positive")
    neg_news = sum(1 for n in news_items if n.get("sentiment") == "negative")
    if pos_news:
        explanation_parts.append(f"{pos_news} positive news articles, +{pos_news*5} to score.")
        feature_contributions["positive_news"] = pos_news * 5
    else:
        feature_contributions["positive_news"] = 0
    if neg_news:
        explanation_parts.append(f"{neg_news} negative news articles, -{neg_news*10} from score.")
        feature_contributions["negative_news"] = -neg_news * 10
    else:
        feature_contributions["negative_news"] = 0

    summary = " ".join(explanation_parts)
    return {"feature_contributions": feature_contributions, "plain_summary": summary}
