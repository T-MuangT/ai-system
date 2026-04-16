from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies import MONGODB_URL
from models.user import User
from models.invoice import Invoice
from models.chat import Chat
from models.customer import Customer
from models.vendor import Vendor
from models.payment import Payment
from models.audit_log import AuditLog
from models.report import Report

async def init_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(database=client.ap_ar_db, document_models=[User, Invoice, Chat, Customer, Vendor, Payment, AuditLog, Report])
