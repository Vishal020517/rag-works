from groq import Groq
import requests
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv()

# 🔑 API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_URL = "https://rag-works.onrender.com"

chat_history = [
    {"role": "system", "content": "You are a helpful financial assistant."}
]

last_intent = None
last_ticker = None


# 🔍 Check stock query
def is_stock_query(query):
    res = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # fast + good enough
        messages=[
            {"role": "system", "content": "Answer YES or NO. Is this about stocks?"},
            {"role": "user", "content": query}
        ]
    )
    return "yes" in res.choices[0].message.content.lower()


# 🔍 Detect ticker
def detect_ticker(query):
    res = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # fast + good enough
        messages=[
            {
                "role": "system",
                "content": "Extract stock ticker or return NONE"
            },
            {"role": "user", "content": query}
        ]
    )
    return res.choices[0].message.content.strip()


# 🔍 Validate ticker
def validate_ticker(ticker):
    try:
        return yf.Ticker(ticker).info.get("regularMarketPrice") is not None
    except:
        return False


# 📄 DOWNLOAD REPORT
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

        print(f"✅ Report saved as {file_name}")

    except Exception as e:
        print(f"❌ Report download failed: {e}")


# 🌐 API CALL
def call_api(query):
    global last_ticker

    ticker = detect_ticker(query)

    if ticker == "NONE":
        return {"type": "non_stock"}

    if not validate_ticker(ticker):
        return {"type": "invalid_ticker"}

    last_ticker = ticker

    print(f"\n📊 Detected Ticker: {ticker}")

    res = requests.get(
        f"{BASE_URL}/analyze",
        params={"ticker": ticker, "query": query}
    )

    return res.json()


# 🤖 CHAT LOOP
def chat():
    global last_intent, last_ticker

    print("🤖 AI Financial Assistant")
    print("Type 'exit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # 🔥 Handle follow-up
        if user_input.lower() in ["yes", "ok", "sure"]:
            if last_ticker:
                user_input = f"details about {last_ticker}"

        # 🔥 REPORT DOWNLOAD TRIGGER
        if "report" in user_input.lower() or "pdf" in user_input.lower():
            if last_ticker:
                download_report(last_ticker)
            else:
                print("⚠️ No stock selected yet.")
            continue

        # 🔥 ROUTING
        if is_stock_query(user_input) or last_intent == "stock":
            last_intent = "stock"

            data = call_api(user_input)

            if data.get("type") == "non_stock":
                prompt = "Explain that this is not a public stock."

            elif data.get("type") == "invalid_ticker":
                prompt = "Ask user to clarify the stock."

            else:
                prompt = f"""
User Query: {user_input}

Data:
{data}

Explain clearly and give recommendation.
"""

        else:
            last_intent = "general"
            prompt = user_input

        chat_history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # fast + good enough
            messages=chat_history
        )

        ai_reply = response.choices[0].message.content

        chat_history.append({"role": "assistant", "content": ai_reply})

        print("\nAI:", ai_reply)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    chat()