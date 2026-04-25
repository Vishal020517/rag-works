import requests

MCP_BASE = "https://rag-works.onrender.com"


# 🔹 STOCK TOOL
def stock_tool(ctx):
    ticker = ctx["ticker"]

    print("📊 Fetching stock data...")

    res = requests.get(f"{MCP_BASE}/stock/{ticker}")
    ctx["stock"] = res.json()

    return ctx


# 🔹 NEWS TOOL
def news_tool(ctx):
    ticker = ctx["ticker"]

    print("📰 Fetching news...")

    res = requests.get(f"{MCP_BASE}/news/{ticker}")
    data = res.json()

    ctx["news"] = data.get("news", [])

    # Extract sentiments safely
    ctx["sentiments"] = [
        article.get("sentiment", "Neutral")
        for article in ctx["news"]
    ]

    return ctx


# 🔹 KPI TOOL
def kpi_tool(ctx):
    print("📈 Calculating KPI...")

    # 🔥 Ensure dependency
    if "stock" not in ctx:
        print("⚠️ Stock missing → fetching first")
        ctx = stock_tool(ctx)

    res = requests.post(
        f"{MCP_BASE}/kpi",
        json=ctx["stock"]
    )

    ctx["kpi"] = res.json()

    return ctx


# 🔹 RISK TOOL
def risk_tool(ctx):
    print("⚠️ Calculating risk...")

    # 🔥 Ensure dependencies
    if "kpi" not in ctx:
        print("⚠️ KPI missing → calculating first")
        ctx = kpi_tool(ctx)

    if "sentiments" not in ctx:
        print("⚠️ News missing → fetching first")
        ctx = news_tool(ctx)

    res = requests.post(
        f"{MCP_BASE}/risk",
        json={
            "pe_ratio": ctx["kpi"]["pe_ratio"],
            "sentiments": ctx["sentiments"]
        }
    )

    ctx["risk"] = res.json()

    return ctx


# 🔹 RECOMMENDATION TOOL
def recommendation_tool(ctx):
    print("🎯 Generating recommendation...")

    # 🔥 Ensure dependencies
    if "risk" not in ctx:
        print("⚠️ Risk missing → calculating first")
        ctx = risk_tool(ctx)

    res = requests.post(
        f"{MCP_BASE}/recommendation",
        json={
            "valuation": ctx["kpi"]["valuation"],
            "risk": ctx["risk"]["risk"]
        }
    )

    ctx["recommendation"] = res.json()

    return ctx


# 🔹 REPORT TOOL (FIXED)
def report_tool(ctx):
    print("📄 Generating report...")

    ticker = ctx["ticker"]

    # ✅ correct endpoint (GET)
    ctx["report_url"] = f"{MCP_BASE}/report?ticker={ticker}"

    return ctx


# 🔹 CHART TOOL
def chart_tool(ctx):
    print("📊 Preparing chart...")

    ticker = ctx["ticker"]

    ctx["chart"] = {
        "type": "stock_chart",
        "ticker": ticker
    }

    return ctx


# 🔥 TOOL REGISTRY
TOOLS = {
    "stock": stock_tool,
    "news": news_tool,
    "kpi": kpi_tool,
    "risk": risk_tool,
    "recommendation": recommendation_tool,
    "report": report_tool,
    "chart": chart_tool
}