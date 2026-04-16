from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.database import init_db
from src.agents.assistance import AssistantAgent
from src.agents.auditor import AuditorAgent
from src.models.invoice import Invoice
from src.models.user import User
from src.models.chat import Chat, ChatMessage
from src.models.customer import Customer
from src.models.vendor import Vendor
from src.models.payment import Payment
from src.models.audit_log import AuditLog
from src.models.report import Report

app = FastAPI()

# Connects your React app (Vite) to this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant_agent = None
auditor_agent = None

@app.on_event("startup")
async def on_startup():
    try:
        await init_db()
        print("Database connected successfully")
    except Exception as e:
        print(f"Database connection failed: {e}")
    
    global assistant_agent, auditor_agent
    try:
        assistant_agent = AssistantAgent()
        print("Assistant agent initialized")
    except ValueError as e:
        print(f"Assistant agent not initialized: {e}")
    try:
        auditor_agent = AuditorAgent()
        print("Auditor agent initialized")
    except ValueError as e:
        print(f"Auditor agent not initialized: {e}")

# Auth endpoints
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/login")
async def login(request: LoginRequest):
    # Simple mock authentication - in real app, verify password hash
    user = await User.find_one(User.email == request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": f"mock_token_{user.id}", "user": user}

@app.get("/users/me")
async def get_current_user():
    # Mock current user - in real app, get from JWT token
    user = await User.find_one()  # Just return first user for now
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Chat request model
class ChatRequest(BaseModel):
    user_msg: str
    user_id: Optional[str] = "default_user"

# Matches 'AI Chat' button in your documentation 
@app.post("/chat")
async def handle_chat(request: ChatRequest):
    if not assistant_agent:
        return {"error": "Chat service not available - API key not configured"}
    
    # Claude processes the user's question
    result = await assistant_agent.run(request.user_msg)
    
    # Save chat to database
    chat = await Chat.find_one(Chat.user_id == request.user_id)
    if not chat:
        chat = Chat(user_id=request.user_id, messages=[])
    
    chat.messages.append(ChatMessage(role="user", content=request.user_msg))
    chat.messages.append(ChatMessage(role="assistant", content=result))
    await chat.save()
    
    return {"ai_message": result}

# Get chat history
@app.get("/chat/{user_id}")
async def get_chat_history(user_id: str):
    chat = await Chat.find_one(Chat.user_id == user_id)
    if not chat:
        return {"messages": []}
    return {"messages": chat.messages}

# Matches 'Dashboard' summary in your documentation 
@app.get("/dashboard/summary")
async def get_summary():
    # Aggregate stats from MongoDB
    total_invoices = await Invoice.count()
    paid_invoices = await Invoice.find(Invoice.status == "paid").count()
    overdue_invoices = await Invoice.find(Invoice.status == "overdue").count()
    
    return {
        "total_invoices": total_invoices,
        "paid_invoices": paid_invoices,
        "overdue_invoices": overdue_invoices
    }

# Invoice endpoints
@app.get("/invoices")
async def get_invoices():
    invoices = await Invoice.find_all().to_list()
    return invoices

@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    await invoice.insert()
    return invoice

@app.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: str):
    invoice = await Invoice.get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@app.put("/invoices/{invoice_id}")
async def update_invoice(invoice_id: str, invoice_data: dict):
    invoice = await Invoice.get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    for key, value in invoice_data.items():
        setattr(invoice, key, value)
    
    await invoice.save()
    return invoice

# Auditor endpoint using DeepSeek
@app.post("/audit")
async def run_audit(task: str = Body(embed=True)):
    if not auditor_agent:
        return {"error": "Audit service not available - API key not configured"}
    
    result = await auditor_agent.run(task)
    return {"audit_result": result}

# User endpoints
@app.get("/users")
async def get_users():
    users = await User.find_all().to_list()
    return users

@app.post("/users")
async def create_user(user: User):
    await user.insert()
    return user

# Invoice approval endpoint
@app.post("/invoices/{invoice_id}/approve")
async def approve_invoice(invoice_id: str):
    invoice = await Invoice.get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.status = "approved"
    await invoice.save()
    
    # Log audit event
    audit_log = AuditLog(
        user_id="system",  # In real app, get from auth
        action="approve_invoice",
        resource_type="invoice",
        resource_id=invoice_id,
        details=f"Invoice {invoice.invoice_number} approved"
    )
    await audit_log.insert()
    
    return invoice

# Payment recording endpoint
@app.post("/invoices/{invoice_id}/payments")
async def record_payment(invoice_id: str, payment: Payment):
    invoice = await Invoice.get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    payment.invoice_id = invoice_id
    await payment.insert()
    
    # Update invoice status if fully paid
    # For simplicity, just mark as paid if payment amount >= invoice amount
    if payment.amount >= invoice.amount:
        invoice.status = "paid"
        await invoice.save()
    
    # Log audit event
    audit_log = AuditLog(
        user_id="system",
        action="record_payment",
        resource_type="payment",
        resource_id=str(payment.id),
        details=f"Payment of ${payment.amount} recorded for invoice {invoice.invoice_number}"
    )
    await audit_log.insert()
    
    return payment

# Payments endpoint
@app.get("/payments")
async def get_payments():
    payments = await Payment.find_all().to_list()
    return payments

# Customers endpoint
@app.get("/customers")
async def get_customers():
    customers = await Customer.find_all().to_list()
    return customers

@app.post("/customers")
async def create_customer(customer: Customer):
    await customer.insert()
    return customer

# Vendors endpoint
@app.get("/vendors")
async def get_vendors():
    vendors = await Vendor.find_all().to_list()
    return vendors

@app.post("/vendors")
async def create_vendor(vendor: Vendor):
    await vendor.insert()
    return vendor

# Reports endpoint
@app.get("/reports")
async def get_reports():
    reports = await Report.find_all().to_list()
    return reports

@app.post("/reports")
async def create_report(report: Report):
    await report.insert()
    return report

# Audit logs endpoint
@app.get("/audit-logs")
async def get_audit_logs():
    audit_logs = await AuditLog.find_all().to_list()
    return audit_logs