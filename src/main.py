import os

import psycopg2
from fastapi import FastAPI, HTTPException

from create_newsletter import create_newsletter, NewsletterRequest

app = FastAPI()


def get_db_connection():
    host = os.getenv("POSTGRES_HOST", "postgres")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    if not database or not user or not password:
        raise HTTPException(status_code=500, detail="Missing PostgreSQL configuration")

    try:
        return psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=5432,
        )
    except psycopg2.Error as exc:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}") from exc

@app.post("/newsletter/create")
def create_newsletter_route(data: NewsletterRequest):
    connection = get_db_connection()
    try:
        return create_newsletter(connection, data)
    finally:
        connection.close()

# @app.post("/deepsearch")
# def deep_search(user_request: str = Body(..., embed=True)):

#     queries = convert_request_to_query(user_request)
#     query = " OR ".join(queries)

#     #Duckduckgo
#     results = []
#     with DDGS() as ddgs:
#         for r in ddgs.text(query, max_results = 20):
#             results.append({
#                 "title": r.get("title", ""),
#                 "url": r.get("url", ""),
#                 "snippet": r.get("body", "")
#             })

#     search_results_text = "\n".join([
#         f"- {r['title']} ({r['url']}): {r['snippet']}"
#         for r in results
#     ])

#     #Llama3
#     prompt = f"""
# You are a news aggregation assistant.
# Based on the user's request, select the most relevant news.
# Return valid JSON only based on the expected JSON format.

# ## User request:
# {user_request}

# ## Search results:
# {search_results_text}

# ## Expected JSON format:
# {{
#   "query": "...",
#   "articles": [
#     {{
#       "title": "...",
#       "url": "...",
#       "summary": "...",
#       "reason": "..."
#     }}
#   ]
# }}
# """
#     response = requests.post(
#         f"{OLLAMA_BASE_URL}/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     data = response.json()
#     raw_text = data.get("response", "")

#     try:
#         return {"data": json.loads(raw_text)}
#     except json.JSONDecodeError:
#         return {
#             "data": {
#                 "query": query,
#                 "raw_response": raw_text,
#                 "raw_results": results
#             }
#         }