import requests

MCP_BASE = "https://rag-works.onrender.com"

def analyst_agent(ticker: str):
    try:
        print("🔵 Analyst Agent started...")

        # Step 1: Get stock data
        stock_res = requests.get(f"{MCP_BASE}/stock/{ticker}")
        stock_data = stock_res.json()

        print("📊 Stock data fetched")

        # Step 2: Get KPI
        kpi_res = requests.post(f"{MCP_BASE}/kpi", json=stock_data)
        kpi_data = kpi_res.json()

        print("📈 KPI calculated")

        return {
            "ticker": ticker,
            "stock": stock_data,
            "kpi": kpi_data
        }

    except Exception as e:
        return {
            "error": "Analyst agent failed",
            "details": str(e)
        }

if __name__ == "__main__":
    result = analyst_agent("AAPL")
    print(result)