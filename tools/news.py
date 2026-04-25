import requests
from groq import Groq
import json
from dotenv import load_dotenv
import os

load_dotenv()


NEWS_API_KEY=os.getenv("NEWS_API_KEY")

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_company_news(company:str):
    url=f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}"

    try:
        response=requests.get(url)
        data=response.json()
        articles=data.get("articles",[])[:5]
        results=[]

        title=[article.get("title") for article in articles]
        sentiments=analyze_sentiment(title)
        results=[]

        for i, article in enumerate(articles):
            results.append({
                "title":article.get("title"),
                "description":article.get("description"),
                "sentiment":sentiments[i]
            })
        return{
            "company":company,
            "news":results
        }
        
    except Exception as e:
        return{
            "message":f"Error fetching news for {company}: {str(e)}"
        }

def analyze_sentiment(titles:str):
    try:
        prompt = f"""
        Classify each of the following news headlines as Positive, Negative, or Neutral.

        Headlines:
        {titles}

        Return ONLY a JSON list like:
        ["Positive", "Negative", "Neutral"]
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # fast + good enough
            messages=[
                {"role": "system", "content": "You are a financial sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        sentiments = json.loads(output)

        # safety check
        if len(sentiments) != len(titles):
            return ["Neutral"] * len(titles)

        return sentiments

    except Exception as e:
        print("LLM Error:", e)
        return ["Neutral"] * len(titles)