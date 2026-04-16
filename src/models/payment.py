from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Payment(Document):
    invoice_id: str
    amount: float
    payment_date: datetime
    payment_method: str  # "check", "wire", "card", etc.
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "payments"