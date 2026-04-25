from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_report(data):
    try:
        # Step 1: Generate report text using LLM
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

        Keep it professional and clear.
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # fast + good enough
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        report_text = response.choices[0].message.content.strip()

        # Step 2: Create PDF
        file_path = "financial_report.pdf"

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        elements = []

        for line in report_text.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 10))

        doc.build(elements)

        # Step 3: Return file info
        return {
            "message": "Report generated successfully",
            "file": file_path
        }

    except Exception as e:
        return {
            "error": "Report generation failed",
            "details": str(e)
        }