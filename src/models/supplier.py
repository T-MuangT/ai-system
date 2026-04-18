from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Supplier(Document):
    supplier_id: str
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "suppliers"