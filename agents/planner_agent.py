from groq import Groq
import json
from dotenv import load_dotenv
import os
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def planner_agent(user_query: str):
    try:
        print("🧠 Planner Agent analyzing query...")

        prompt = f"""
            You are an AI planner for a financial system.

            Decide steps BASED ON USER INTENT.

            Rules:

            If user asks:
            - "stock price / details" → ["stock"]
            - "news / latest news" → ["news"]
            - "kpi / metrics" → ["stock", "kpi"]
            - "risk" → ["stock", "kpi", "risk"]
            - "should I buy / recommendation" → ["stock", "kpi", "risk", "recommendation"]
            - "full analysis" → ["stock", "news", "kpi", "risk", "recommendation"]
            - "report / pdf" → ["stock", "kpi", "risk", "recommendation", "report"]
            - "chart" → ["chart"]

            Return ONLY JSON like:
            [
            {{"step": "stock"}},
            {{"step": "news"}}
            ]

            Query: "{user_query}"
            """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # fast + good enough
            messages=[
                {"role": "system", "content": "You are a planning agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        print("📋 Plan generated:", output)

        return json.loads(output)

    except Exception as e:
        print("Planner error:", e)
        return ["stock", "kpi"]  # fallback