def calculate_kpis(stock_data):
    try:
        price=stock_data.get("price")
        market_cap=stock_data.get("market_cap")
        pe_ratio=stock_data.get("pe_ratio")

        valuation="fair"

        if pe_ratio:
            if pe_ratio>30:
                valuation="overvalued"
            elif pe_ratio<15:
                valuation="undervalued"
            
        size="mid cap"

        if market_cap:
            if market_cap>1e12:
                size="large cap"
            elif market_cap < 1e10:
                size = "small cap"
        
        return{
            "price":price,
            "pe_ratio":pe_ratio,
            "market_cap":market_cap,
            "valuation":valuation,
            "company_size":size
        }
    
    except Exception as e:
        return{
            "message":f"Error calculating KPIs: {str(e)}"
        }

            