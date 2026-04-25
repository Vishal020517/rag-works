from groq import Groq
from agents.orchestrator import run_dynamic_agent
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_URL = "https://rag-works.onrender.com"

chat_history = [
    {"role": "system", "content": "You are a helpful financial assistant."}
]

last_intent = None
last_ticker = None


# 🔍 Check if stock-related
def is_stock_query(query):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast + good enough
        messages=[
            {"role": "system", "content": "Answer YES or NO. Is this about stocks, finance or investing?"},
            {"role": "user", "content": query}
        ]
    )
    return "yes" in res.choices[0].message.content.lower()


# 🔍 Dynamic ticker detection (NO HARDCODING)
def detect_ticker(query):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast + good enough
        messages=[
            {
                "role": "system",
                "content": """
Extract stock ticker.

Rules:
- Return ONLY ticker (e.g., AAPL, TSLA)
- If brand → map to company (Redmi → Xiaomi)
- If not public → return NONE
"""
            },
            {"role": "user", "content": query}
        ]
    )

    return res.choices[0].message.content.strip()


# 📄 Download report
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


# 🤖 MAIN CHAT
def chat():
    global last_intent, last_ticker

    print("🤖 AI Financial Assistant (Dynamic + MCP)")
    print("Type 'exit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # 🔥 Handle follow-up
        if user_input.lower() in ["yes", "ok", "sure"]:
            if last_ticker:
                user_input = f"Give full details about {last_ticker}"

        # 🔥 Detect ticker dynamically
        ticker = detect_ticker(user_input)

        if ticker != "NONE":
            last_ticker = ticker
        else:
            ticker = last_ticker

        # ❌ No ticker found
        if not ticker:
            print("⚠️ Please specify a stock.")
            continue

        print(f"📊 Using ticker: {ticker}")

        # 🔥 Report trigger
        if "report" in user_input.lower() or "pdf" in user_input.lower():
            download_report(ticker)
            continue

        # 🔥 Check intent
        if is_stock_query(user_input):
            last_intent = "stock"

            # 🔥 CALL YOUR AGENT SYSTEM (IMPORTANT)
            context = run_dynamic_agent(user_input, ticker)

            print("🧠 CONTEXT:", context)

            # 🔥 FINAL RESPONSE (STRICT MODE)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # fast + good enough
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a financial assistant.

STRICT RULES:
- ONLY use the provided data
- DO NOT add extra assumptions
- DO NOT invent KPI, risk, recommendation
- If missing, say "data not available"
"""
                    },
                    {
                        "role": "user",
                        "content": f"""
User Query: {user_input}

Available Data:
{context}

Answer strictly based on this data.
"""
                    }
                ]
            )

            ai_reply = response.choices[0].message.content

        else:
            last_intent = "general"

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # fast + good enough
                messages=chat_history + [{"role": "user", "content": user_input}]
            )

            ai_reply = response.choices[0].message.content

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": ai_reply})

        print("\nAI:", ai_reply)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    chat()