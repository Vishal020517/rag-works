import requests

MCP_BASE = "https://rag-works.onrender.com"

def research_agent(company: str):
    try:
        print("Research Agent started...")

        res = requests.get(f"{MCP_BASE}/news/{company}")
        data = res.json()

        print("News fetched")

        articles = data.get("news", [])

        sentiments = [
            (a.get("sentiment") or "Neutral")
            for a in articles
        ]

        print("Sentiment extracted")

        pos = sum(1 for s in sentiments if s.lower() == "positive")
        neg = sum(1 for s in sentiments if s.lower() == "negative")
        neu = sum(1 for s in sentiments if s.lower() == "neutral")

        return {
            "company": company,
            "news": articles,
            "sentiments": sentiments,
            "summary": {
                "positive": pos,
                "negative": neg,
                "neutral": neu
            }
        }

    except Exception as e:
        return {
            "error": "Research agent failed",
            "details": str(e)
        }