import os

from fastapi import FastAPI, Body

from db.get_db_connection import get_db_connection

from newsletter.create_newsletter import create_newsletter
from newsletter.schemas import NewsletterRequest
from newsletter.update_preferences import update_preferences
from newsletter.unsubscribe import unsubscribe

from user.delete_user_data import delete_user_data

app = FastAPI()

connection = get_db_connection()

@app.post("/newsletter/create")
def create_newsletter_route(data: NewsletterRequest):
    connection = get_db_connection()
    try:
        return create_newsletter(connection, data)
    finally:
        connection.close()


@app.patch("/newsletter/preferences")
def update_preferences_route(data: NewsletterRequest):
    connection = get_db_connection()
    try:
        return update_preferences(connection, data)
    finally:
        connection.close()

@app.post("/newsletter/unsubscribe")
def unsubscribe_route(session_id: str = Body(..., embed=True)):
    connection = get_db_connection()
    try:
        return unsubscribe(connection, session_id)
    finally:
        connection.close()

@app.delete("/user/delete-data")
def delete_user_data_route(session_id: str = Body(..., embed=True)):
    connection = get_db_connection()
    try:
        return delete_user_data(connection, session_id)
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