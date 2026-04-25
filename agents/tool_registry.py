import requests

MCP_BASE = "http://127.0.0.1:8000"

def stock_tool(ctx):
    ticker = ctx["ticker"]
    res = requests.get(f"{MCP_BASE}/stock/{ticker}")
    data = res.json()
    ctx["stock"] = data
    return ctx

def news_tool(ctx):
    ticker = ctx["ticker"]
    res = requests.get(f"{MCP_BASE}/news/{ticker}")
    data = res.json()
    ctx["news"] = data.get("news", [])
    ctx["sentiments"] = [
        a.get("sentiment", "Neutral") for a in ctx["news"]
    ]
    return ctx

def kpi_tool(ctx):
    res = requests.post(f"{MCP_BASE}/kpi", json=ctx["stock"])
    ctx["kpi"] = res.json()
    return ctx

def risk_tool(ctx):
    res = requests.post(
        f"{MCP_BASE}/risk",
        json={
            "pe_ratio": ctx["kpi"]["pe_ratio"],
            "sentiments": ctx["sentiments"]
        }
    )
    ctx["risk"] = res.json()
    return ctx

def recommendation_tool(ctx):
    res = requests.post(
        f"{MCP_BASE}/recommendation",
        json={
            "valuation": ctx["kpi"]["valuation"],
            "risk": ctx["risk"]["risk"]
        }
    )
    ctx["recommendation"] = res.json()
    return ctx

def report_tool(ctx):
    requests.post(
        f"{MCP_BASE}/report",
        json={
            "stock": ctx["stock"],
            "kpi": ctx["kpi"],
            "risk": ctx["risk"],
            "recommendation": ctx["recommendation"],
            "news": ctx["news"]
        }
    )
    ctx["report"] = "generated"
    return ctx

def chart_tool(ctx):
    ticker = ctx["ticker"]

    ctx["chart"] = {
        "type": "stock_chart",
        "ticker": ticker
    }

    return ctx


TOOLS = {
    "stock": stock_tool,
    "news": news_tool,
    "kpi": kpi_tool,
    "risk": risk_tool,
    "recommendation": recommendation_tool,
    "report": report_tool,
    "chart": chart_tool
}