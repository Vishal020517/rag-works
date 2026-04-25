import yfinance as yf

def get_stock_data(ticker):
    try:
        stock=yf.Ticker(ticker)
        info=stock.info
        return{
            "company":info.get("longName"),
            "price":info.get("currentPrice"),
            "market_cap":info.get("marketCap"),
            "pe_ratio":info.get("trailingPE"),
        }
    except Exception as e:
        return{
            "message":f"Error fetching data for {ticker}: {str(e)}"
        }