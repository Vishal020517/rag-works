from groq import Groq
from agents.orchestrator import run_dynamic_agent
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_URL = "https://rag-works.onrender.com"

chat_history = [
    {"role": "system", "content": "You are a helpful financial assistant."}
]

last_intent = None
last_ticker = None

def is_stock_query(query):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {"role": "system", "content": "You are a classifier. Respond with ONLY 'YES' or 'NO'. No other text."},
            {"role": "user", "content": f"Is this about stocks, finance, investing, or company financials? Query: {query}"}
        ]
    )
    answer = res.choices[0].message.content.strip().upper()

    if "YES" in answer:
        print(f"DEBUG: Is stock query? YES for '{query}'")  
        return True
    else:
        print(f"DEBUG: Is stock query? NO for '{query}'")  
        return False

def detect_ticker(query):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {
                "role": "system",
                "content": "Extract ONLY the stock ticker symbol. Output format: SINGLE TICKER OR NONE. No other text."
            },
            {
                "role": "user",
                "content": f"""Extract ticker from: {query}

Mappings:
- Apple/apple → AAPL
- Tesla/tesla → TSLA  
- Google/google → GOOGL
- Microsoft/microsoft → MSFT
- Amazon/amazon → AMZN
- Meta/meta → META
- Nvidia/nvidia → NVDA

Return ONLY: TICKER or NONE"""
            }
        ]
    )

    response = res.choices[0].message.content.strip().upper()
    # Extract only valid ticker symbols (1-5 uppercase letters)
    import re
    match = re.search(r'\b([A-Z]{1,5})\b', response)
    ticker = match.group(1) if match else "NONE"
    
    print(f"DEBUG: Detected ticker: '{ticker}' for '{query}'")  # Debug print
    return ticker



def download_report(ticker):
    try:
        print(f"\n📄 Downloading report for {ticker}...")

        response = requests.get(
            f"{BASE_URL}/report",
            params={"ticker": ticker},
            timeout=60
        )

        file_name = f"{ticker}_report.pdf"

        with open(file_name, "wb") as f:
            f.write(response.content)

        print(f"Report saved as {file_name}")

    except Exception as e:
        print(f"Report download failed: {e}")



def chat():
    global last_intent, last_ticker

    print("🤖 AI Financial Assistant (Dynamic + MCP)")
    print("Type 'exit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

      
        if user_input.lower() in ["yes", "ok", "sure"]:
            if last_ticker:
                user_input = f"Give full details about {last_ticker}"

    
        is_stock = is_stock_query(user_input)
        
        if is_stock:
            ticker = detect_ticker(user_input)

            if ticker != "NONE":
                last_ticker = ticker
            else:
                ticker = last_ticker

    
            if not ticker:
                print("⚠️ Please specify a stock.")
                continue

            print(f"📊 Using ticker: {ticker}")

            
            if "report" in user_input.lower() or "pdf" in user_input.lower():
                if ticker and ticker != "NONE":
                    download_report(ticker)
                else:
                    print("Please specify a stock ticker for report generation.")
                continue

            last_intent = "stock"
            print("DEBUG: Calling agent for stock query")

             
            context = run_dynamic_agent(user_input, ticker)

            print("CONTEXT:", context)

            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a professional financial analyst. Your job is to present data from the context in a clear, 
beautiful, and understandable way while maintaining 100% accuracy.

RULES:
1. Base ALL insights ONLY on the provided data - never invent or assume
2. Use professional formatting: headers, bullet points, bold text for emphasis
3. Explain metrics in simple terms so non-technical users understand
4. Provide context for numbers (e.g., explain what PE ratio value means)
5. Organize information logically with clear sections
6. Use analogies or relatable examples to explain concepts
7. Highlight key findings that matter for decision-making
8. If data contradicts a claim, report the data as-is (valuation='fair' means report it as fair, don't reinterpret)

PRESENTATION GUIDELINES:
- Use ** for headers and important terms
- Group related information together
- Provide summary at the top, details below
- Make numbers easy to understand (add context like "industry average" if in data)
- Use clear language, avoid jargon where possible
- Add a brief interpretation line for each metric based on the provided values

EXAMPLE FORMAT:
**Stock Price & Valuation**
- Current Price: $XXX.XX
- This represents the current market value of the stock
- PE Ratio: X.XX [if data says fair/overvalued/undervalued, use that exact word]
- Interpretation: [Explain what this PE ratio means based on the valuation field in data]

**Company Profile**
- [Describe company size, market cap implications based on provided data]

Always source your insights directly from the available data context provided.
"""
                    },
                    {
                        "role": "user",
                        "content": f"""
User Query: {user_input}

Available Data:
{json.dumps(context, indent=2)}

Provide a response based ONLY on the above data.
"""
                    }
                ]
            )

            ai_reply = response.choices[0].message.content

        else:
            last_intent = "general"
            print("DEBUG: Using general Groq response") 

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=chat_history + [{"role": "user", "content": user_input}]
            )

            ai_reply = response.choices[0].message.content

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": ai_reply})

        print("\nAI:", ai_reply)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    chat()