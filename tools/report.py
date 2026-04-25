from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

# 🔑 Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🌐 Your deployed API
BASE_URL = "https://rag-works.onrender.com"


# 🔥 CLEAN TEXT FUNCTION (CRITICAL FIX)
def clean_text(text):
    # Replace <br> with newline
    text = text.replace("<br>", "\n")

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove markdown tables
    text = re.sub(r"\|.*?\|", "", text)

    # Remove bold markdown
    text = text.replace("**", "")

    return text


# 🚀 MAIN FUNCTION
def generate_report(ticker):
    try:
        print("STEP 1: Fetching stock data...")

        response = requests.get(
            f"{BASE_URL}/analyze",
            params={"ticker": ticker, "query": "Generate report"},
            timeout=60
        )

        data = response.json()
        print("STEP 2: Data fetched")

        # 🔥 LLM Prompt (clean output)
        prompt = f"""
Generate a detailed financial report.

IMPORTANT:
- DO NOT use HTML tags
- DO NOT use <br>
- DO NOT use markdown tables (|)
- Use simple paragraphs

Data:
{data}

Include:
- Summary
- Key Insights
- Risk Analysis
- Recommendation
- Conclusion
"""

        print("STEP 3: Calling LLM...")

        llm_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # fast + good enough
            messages=[
                {"role": "system", "content": "You are a professional financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        report_text = llm_response.choices[0].message.content.strip()

        # 🔥 CLEAN TEXT (IMPORTANT)
        report_text = clean_text(report_text)

        print("STEP 4: Creating PDF...")

        file_path = f"{ticker}_report.pdf"

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        elements = []

        # 🔥 SAFE PARAGRAPH HANDLING
        for line in report_text.split("\n"):
            if line.strip():
                try:
                    elements.append(Paragraph(line, styles["Normal"]))
                    elements.append(Spacer(1, 10))
                except:
                    elements.append(Paragraph("Formatting issue fixed.", styles["Normal"]))

        doc.build(elements)

        print("STEP 5: PDF created successfully")

        return file_path

    except Exception as e:
        print("❌ REPORT ERROR:", e)
        return None