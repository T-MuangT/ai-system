from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Invoice(Document):
    invoice_number: str
    vendor: str
    amount: float
    due_date: datetime
    status: str  # "pending", "paid", "overdue"
    description: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "invoices"
