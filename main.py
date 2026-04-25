from fastapi import FastAPI
from agents.orchestrator import run_dynamic_agent
from tools.stock import get_stock_data
from tools.news import get_company_news
from tools.kpi import calculate_kpis
from tools.risk import calculate_risk
from tools.recommendation import generate_recommendation
from tools.report import generate_report
from fastapi.responses import FileResponse
from agents.orchestrator import run_dynamic_agent
import os

app=FastAPI()

@app.get("/")
def home():
    return {"message":"MCP Server is running!"}

@app.get("/stock/{ticker}")
def stock(ticker:str):
    return get_stock_data(ticker)

@app.get("/news/{company}")
def news(company:str):
    return get_company_news(company)

@app.post("/kpi")
def kpi(data:dict):
    return calculate_kpis(data)

@app.post("/risk")
def risk(data: dict):
    pe_ratio = data.get("pe_ratio")
    sentiments = data.get("sentiments", [])
    return calculate_risk(pe_ratio,sentiments)

@app.post("/recommendation")
def recommendation(data:dict):
    valuation=data.get("valuation")
    risk=data.get("risk")
    return generate_recommendation(valuation,risk)

@app.get("/report")
def get_report(ticker: str):
    file_path = generate_report(ticker)

    if not file_path or not os.path.exists(file_path):
        return {"error": "Report generation failed"}

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{ticker}_report.pdf"
    )

@app.get("/analyze")
def analyze(ticker: str, query: str):
    return run_dynamic_agent(query, ticker)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



