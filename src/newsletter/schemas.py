from typing import Optional
from pydantic import BaseModel

class NewsletterRequest(BaseModel):
    session_id: str
    topics: Optional[list[str]]
    frequency: Optional[str]
    send_day: Optional[str]
    send_day_of_month: Optional[int]
    send_time: Optional[str]
    tone: Optional[str]
    length: Optional[str]
    format: Optional[str]
    max_articles: Optional[int]
    topics_action: Optional[str]