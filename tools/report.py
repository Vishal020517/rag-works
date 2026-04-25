from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv
import requests

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_URL = "https://rag-works.onrender.com"


def generate_report(ticker):
    try:
        # 🔥 Step 1: Get data from your API
        response = requests.get(
            f"{BASE_URL}/analyze",
            params={"ticker": ticker, "query": "Generate report"}
        )

        data = response.json()

        # 🔥 Step 2: Generate report text
        prompt = f"""
        Generate a detailed financial report.

        Data:
        {data}

        Include:
        - Summary
        - Key Insights
        - Risk Analysis
        - Recommendation
        - Conclusion
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # ✅ correct model
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        report_text = response.choices[0].message.content.strip()

        # 🔥 Step 3: Create PDF (dynamic name)
        file_path = f"{ticker}_report.pdf"

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        elements = []

        for line in report_text.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 10))

        doc.build(elements)

        return file_path  # ✅ return only path

    except Exception as e:
        print("REPORT ERROR:", e)
        return None