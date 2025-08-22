def explain_score(financials, news_items, score):
    """
    Enhanced, backward-compatible explainability:
    - Same signature and return keys.
    - Adds time-decayed news impact (recent news matters more).
    - Robust casting and None-safe checks.
    - Adds an 'other_adjustments' term so feature contributions sum to `score`
      (assuming a base of BASE_SCORE).
    """
    from datetime import datetime, timezone


    # --- Config (keep in sync with your scoring function) ---
    BASE_SCORE = 50.0
    W_NET_INCOME_POS = 18.0
    W_DEBT_RATIO_LOW = 16.0
    W_REVENUE_LARGE = 8.0
    NEWS_POS_UNIT = 4.0
    NEWS_NEG_UNIT = -8.0
    NEWS_HALFLIFE_DAYS = 7.0  # exponential half-life for decay

    # --- Helpers (local to keep this truly drop-in) ---
    def _to_float(x):
        try:
            if x is None:
                return None
            return float(x)
        except Exception:
            return None

    def _exp_decay_weight(days, halflife):
        # weight = 0.5 ** (days / halflife); future or missing dates -> near 0
        if days is None or days < 0:
            return 0.0
        return 0.5 ** (days / max(halflife, 1e-6))

    def _parse_iso_date(d):
        if not d:
            return None
        try:
            # accept 'Z' suffix or offset-naive; normalize to UTC
            d = d.replace("Z", "+00:00")
            dt = datetime.fromisoformat(d)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except Exception:
            return None

    # normalize inputs
    financials = financials or {}
    news_items = news_items or []

    explanation_parts = []
    feature_contributions = {}

    # ----------------------------
    # Financial features (robust)
    # ----------------------------
    net_income = _to_float(financials.get("net_income"))
    debt_ratio = _to_float(financials.get("debt_ratio"))
    revenue = _to_float(financials.get("revenue"))

    # Net income
    if net_income is None:
        feature_contributions["net_income"] = 0.0
        explanation_parts.append("ℹ️ Net income data not available → +0")
    elif net_income > 0:
        feature_contributions["net_income"] = W_NET_INCOME_POS
        explanation_parts.append(f"✅ Net income is positive → +{int(W_NET_INCOME_POS)}")
    else:
        feature_contributions["net_income"] = 0.0
        explanation_parts.append("❌ Net income is negative or zero → +0")

    # Debt ratio
    if debt_ratio is None:
        feature_contributions["debt_ratio"] = 0.0
        explanation_parts.append("ℹ️ Debt ratio data not available → +0")
    elif debt_ratio < 0.5:
        feature_contributions["debt_ratio"] = W_DEBT_RATIO_LOW
        explanation_parts.append(f"✅ Debt ratio is low (<0.5) → +{int(W_DEBT_RATIO_LOW)}")
    else:
        feature_contributions["debt_ratio"] = 0.0
        explanation_parts.append("❌ Debt ratio is high (≥0.5) → +0")

    # Revenue
    if revenue is None:
        feature_contributions["revenue"] = 0.0
        explanation_parts.append("ℹ️ Revenue data not available → +0")
    elif revenue > 1_000_000_000:
        feature_contributions["revenue"] = W_REVENUE_LARGE
        explanation_parts.append(f"✅ Revenue is very high (>1B) → +{int(W_REVENUE_LARGE)}")
    else:
        feature_contributions["revenue"] = 0.0
        explanation_parts.append("❌ Revenue is below threshold (≤1B) → +0")

    # ----------------------------
    # News (time-decayed sentiment)
    # ----------------------------
    now = datetime.now(timezone.utc)
    pos_impact_sum = 0.0
    neg_impact_sum = 0.0
    pos_count = 0
    neg_count = 0

    for n in news_items:
        sent = (n.get("sentiment") or "").strip().lower()
        dt = _parse_iso_date(n.get("date"))
        days_old = (now - dt).days if dt else None
        decay = _exp_decay_weight(days_old, NEWS_HALFLIFE_DAYS)

        if sent == "positive":
            pos_count += 1
            pos_impact_sum += NEWS_POS_UNIT * decay
        elif sent == "negative":
            neg_count += 1
            neg_impact_sum += NEWS_NEG_UNIT * decay
        # neutral/unknown → 0 impact

    # Round for tidy UI, but keep numeric precision reasonable
    pos_impact_sum = round(pos_impact_sum, 2)
    neg_impact_sum = round(neg_impact_sum, 2)

    feature_contributions["positive_news"] = pos_impact_sum
    feature_contributions["negative_news"] = neg_impact_sum

    if pos_count > 0:
        explanation_parts.append(f"✅ {pos_count} positive news (time-decayed) → {pos_impact_sum:+}")
    else:
        explanation_parts.append("❌ No positive news articles → +0")

    if neg_count > 0:
        explanation_parts.append(f"⚠️ {neg_count} negative news (time-decayed) → {neg_impact_sum:+}")
    else:
        explanation_parts.append("✅ No negative news articles → +0")

    # ----------------------------
    # Residual so bars ≈ score
    # ----------------------------
    # If upstream scoring adds pieces not modeled here, attribute the remainder.
    total = sum(feature_contributions.values())
    residual = float(score) - (BASE_SCORE + float(total))
    if abs(residual) >= 0.01:
        residual = round(residual, 2)
        feature_contributions["other_adjustments"] = residual
        explanation_parts.append(f"🔧 Other adjustments (alignment) → {residual:+}")

    # ----------------------------
    # Final summary
    # ----------------------------
    plain_summary = "\n".join(explanation_parts)
    final_text = f"📊 Final Score: {score}\n\nBreakdown:\n{plain_summary}"

    return {
        "feature_contributions": feature_contributions,
        "plain_summary": final_text
    }