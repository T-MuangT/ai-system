from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Customer(Document):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "customers"