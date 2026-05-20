import os
import requests
import json


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

def convert_request_to_query(user_request: str):
    
    prompt = f"""
You are a query generation assistant.

Convert the user's request into web search queries for a news aggregation system.

Rules:
- Return JSON only based on the expected JSON format below
- No explanations
- Focus on recent news
- Generate 3 concise search queries max
- Queries must be useful for a search engine

User request:
{user_request}

Expected JSON format:
{{
  "queries": [
    "query 1",
    "query 2",
    "query 3"
  ]
}}
"""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    raw_output = response.json().get("response", "")

    try:
        data = json.loads(raw_output)
        return data["queries"]
    except Exception:
        return [user_request]
