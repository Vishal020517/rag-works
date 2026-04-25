from groq import Groq
from dotenv import load_dotenv
import os       

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔹 LLM Explanation Function
def explain_recommendation(valuation, risk, recommendation):
    try:
        prompt = f"""
        Explain in 2-3 lines why the recommendation is '{recommendation}'
        given:
        - valuation: {valuation}
        - risk: {risk}

        Keep it simple and financial.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # fast + good enough
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return "Explanation not available"


# 🔹 Main Recommendation Function
def generate_recommendation(valuation, risk):
    try:
        # Step 1: Rule-based decision
        recommendation = "hold"

        if risk == "high":
            recommendation = "sell"
        elif risk == "medium":
            recommendation = "hold"
        elif risk == "low":
            if valuation == "undervalued":
                recommendation = "buy"
            else:
                recommendation = "hold"

        # Step 2: LLM explanation
        explanation = explain_recommendation(valuation, risk, recommendation)

        # Step 3: Return structured output
        return {
            "valuation": valuation,
            "risk": risk,
            "recommendation": recommendation,
            "reason": explanation
        }

    except Exception as e:
        return {
            "error": "Recommendation failed",
            "details": str(e)
        }