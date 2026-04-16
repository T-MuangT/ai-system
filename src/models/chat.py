from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.utcnow()

class Chat(Document):
    user_id: str
    messages: List[ChatMessage] = []
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "chats"
