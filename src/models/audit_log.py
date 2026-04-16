from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditLog(Document):
    user_id: str
    action: str  # "login", "create_invoice", "approve_invoice", etc.
    resource_type: str  # "invoice", "payment", "user", etc.
    resource_id: Optional[str] = None
    details: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

    class Settings:
        name = "audit_logs"