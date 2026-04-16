from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    email: EmailStr
    name: str
    role: str  # e.g., "admin", "user"
    is_active: bool = True

    class Settings:
        name = "users"
