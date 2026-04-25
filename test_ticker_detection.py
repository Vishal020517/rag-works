from groq_chat import detect_ticker, is_stock_query

# Test ticker detection
test_queries = [
    "okk can u generate me an report about the tsla stocks",
    "tell me about tesla",
    "what's the news on AAPL",
    "i need apple stock data",
    "tsla stocks today",
    "can you tell me about microsoft",
]

print("Testing Ticker Detection:")
print("=" * 60)
for query in test_queries:
    ticker = detect_ticker(query)
    is_stock = is_stock_query(query)
    print(f"Query: {query}")
    print(f"  → Ticker: {ticker}")
    print(f"  → Is Stock Query: {is_stock}")
    print()
