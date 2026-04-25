def calculate_risk(pe_ratio, sentiments):
    try:
        positive = sentiments.count("Positive")
        negative = sentiments.count("Negative")

        risk = "medium"

        if pe_ratio and pe_ratio > 30 and negative > positive:
            risk = "high"
        elif pe_ratio and pe_ratio < 15 and positive > negative:
            risk = "low"

        return {
            "pe_ratio": pe_ratio,
            "positive_news": positive,
            "negative_news": negative,
            "risk": risk
        }

    except Exception as e:
        return {
            "error": "Risk calculation failed",
            "details": str(e)
        }