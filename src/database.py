from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.dependencies import MONGODB_URL
from src.models.user import User
from src.models.invoice import Invoice
from src.models.chat import Chat
from src.models.customer import Customer
from src.models.vendor import Vendor
from src.models.payment import Payment
from src.models.audit_log import AuditLog
from src.models.report import Report

async def init_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(database=client.ap_ar_db, document_models=[User, Invoice, Chat, Customer, Vendor, Payment, AuditLog, Report])
