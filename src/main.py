import json
import os
import requests

from convert_request_to_query import convert_request_to_query

from fastapi import FastAPI, Body
from ddgs import DDGS
from pydantic import BaseModel
import pandas as pd


app = FastAPI()


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

@app.post("/deepsearch")
def deep_search(user_request: str = Body(..., embed=True)):

    queries = convert_request_to_query(user_request)
    query = " OR ".join(queries)

    #Duckduckgo
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results = 20):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("body", "")
            })

    search_results_text = "\n".join([
        f"- {r['title']} ({r['url']}): {r['snippet']}"
        for r in results
    ])

    #Llama3
    prompt = f"""
You are a news aggregation assistant.
Based on the user's request, select the most relevant news.
Return valid JSON only based on the expected JSON format.

## User request:
{user_request}

## Search results:
{search_results_text}

## Expected JSON format:
{{
  "query": "...",
  "articles": [
    {{
      "title": "...",
      "url": "...",
      "summary": "...",
      "reason": "..."
    }}
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

    data = response.json()
    raw_text = data.get("response", "")

    try:
        return {"data": json.loads(raw_text)}
    except json.JSONDecodeError:
        return {
            "data": {
                "query": query,
                "raw_response": raw_text,
                "raw_results": results
            }
        }