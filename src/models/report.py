from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class Report(Document):
    name: str
    type: str  # "aging", "vendor_summary", "customer_summary", etc.
    parameters: Dict[str, Any] = {}
    data: Dict[str, Any] = {}
    generated_at: datetime = datetime.utcnow()
    generated_by: str  # user_id

    class Settings:
        name = "reports"