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

        Available steps:
        - stock
        - news
        - kpi
        - risk
        - recommendation
        - report
        - chart

        Return a JSON array of steps in order.

        Example:
        [
        {{"step": "stock"}},
        {{"step": "news"}},
        {{"step": "kpi"}},
        {{"step": "risk"}},
        {{"step": "recommendation"}},
        {{"step": "report"}},
        {{"step": "chart"}}
        ]

        Query: "{user_query}"

        ONLY return JSON.
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # fast + good enough
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