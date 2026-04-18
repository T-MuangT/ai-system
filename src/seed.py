import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

MONGODB_URL = "mongodb://localhost:27017/"

async def seed():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client["ap_ar_db"]

    # Clear existing data
    await db.invoices.drop()
    await db.suppliers.drop()
    await db.vendors.drop()
    await db.payments.drop()
    await db.users.drop()

    print("🗑️  Cleared existing data...")

    # ── USERS ──────────────────────────────────────────────────────────────
    await db.users.insert_many([
        {
            "user_id": "USR-1",
            "email": "admin@apcompass.com",
            "name": "Sarah Mitchell",
            "role": "admin",
            "is_active": True,
        },
        {
            "user_id": "USR-2",
            "email": "manager@apcompass.com",
            "name": "James Thornton",
            "role": "manager",
            "is_active": True,
        },
        {
            "user_id": "USR-3",
            "email": "emp1@apcompass.com",
            "name": "Priya Nair",
            "role": "employee",
            "is_active": True,
        },
        {
            "user_id": "USR-4",
            "email": "emp2@apcompass.com",
            "name": "Carlos Rivera",
            "role": "employee",
            "is_active": True,
        },
    ])
    print("✅ Users seeded")

    # ── SUPPLIERS ──────────────────────────────────────────────────────────
    await db.suppliers.insert_many([
        {
            "supplier_id": "SUP-1",
            "name": "Acme Corp",
            "email": "billing@acme.com",
            "phone": "555-0101",
            "address": "123 Main St, New York, NY",
            "created_at": datetime.utcnow(),
        },
        {
            "supplier_id": "SUP-2",
            "name": "Globex Ltd",
            "email": "ap@globex.com",
            "phone": "555-0102",
            "address": "456 Oak Ave, Chicago, IL",
            "created_at": datetime.utcnow(),
        },
        {
            "supplier_id": "SUP-3",
            "name": "Initech",
            "email": "finance@initech.com",
            "phone": None,
            "address": None,
            "created_at": datetime.utcnow(),
        },
        {
            "supplier_id": "SUP-4",
            "name": "Umbrella Trading",
            "email": "procurement@umbrella.com",
            "phone": "555-0201",
            "address": "789 Corporate Blvd, Houston, TX",
            "created_at": datetime.utcnow(),
        },
        {
            "supplier_id": "SUP-5",
            "name": "Stark Industries",
            "email": "accounts@stark.com",
            "phone": "555-0202",
            "address": "10880 Malibu Point, Los Angeles, CA",
            "created_at": datetime.utcnow(),
        },
        {
            "supplier_id": "SUP-6",
            "name": "Wayne Enterprises",
            "email": "finance@wayneent.com",
            "phone": "555-0203",
            "address": "1007 Mountain Drive, Gotham, NJ",
            "created_at": datetime.utcnow(),
        },
    ])
    print("✅ Suppliers seeded")

    # ── VENDORS ────────────────────────────────────────────────────────────
    await db.vendors.insert_many([
        {
            "vendor_id": "VND-1",
            "name": "Office Supplies Co",
            "email": "invoices@officesupplies.com",
        },
        {
            "vendor_id": "VND-2",
            "name": "Cloud Hosting Inc",
            "email": "billing@cloudhosting.com",
        },
        {
            "vendor_id": "VND-3",
            "name": "FastFreight Logistics",
            "email": "ap@fastfreight.com",
        },
        {
            "vendor_id": "VND-4",
            "name": "TechParts Direct",
            "email": "orders@techparts.com",
        },
        {
            "vendor_id": "VND-5",
            "name": "CleanSpace Facilities",
            "email": "invoices@cleanspace.com",
        },
    ])
    print("✅ Vendors seeded")

    # ── INVOICES (20 total) ────────────────────────────────────────────────
    now = datetime.utcnow()
    await db.invoices.insert_many([
        # PAID
        {
            "invoice_number": "INV-001",
            "vendor": "Office Supplies Co",
            "amount": 5000.00,
            "due_date": now - timedelta(days=40),
            "status": "paid",
            "description": "Q1 office supplies order",
            "created_at": now - timedelta(days=60),
        },
        {
            "invoice_number": "INV-002",
            "vendor": "Cloud Hosting Inc",
            "amount": 12500.00,
            "due_date": now - timedelta(days=30),
            "status": "paid",
            "description": "Annual cloud infrastructure license",
            "created_at": now - timedelta(days=50),
        },
        {
            "invoice_number": "INV-003",
            "vendor": "FastFreight Logistics",
            "amount": 3800.00,
            "due_date": now - timedelta(days=25),
            "status": "paid",
            "description": "March shipment batch — 14 pallets",
            "created_at": now - timedelta(days=45),
        },
        {
            "invoice_number": "INV-004",
            "vendor": "TechParts Direct",
            "amount": 7200.00,
            "due_date": now - timedelta(days=20),
            "status": "paid",
            "description": "Server RAM and SSD upgrade kit",
            "created_at": now - timedelta(days=35),
        },
        {
            "invoice_number": "INV-005",
            "vendor": "CleanSpace Facilities",
            "amount": 1500.00,
            "due_date": now - timedelta(days=15),
            "status": "paid",
            "description": "Monthly office cleaning — March",
            "created_at": now - timedelta(days=30),
        },
        # OVERDUE
        {
            "invoice_number": "INV-006",
            "vendor": "Cloud Hosting Inc",
            "amount": 9800.00,
            "due_date": now - timedelta(days=12),
            "status": "overdue",
            "description": "Q2 cloud storage expansion",
            "created_at": now - timedelta(days=25),
        },
        {
            "invoice_number": "INV-007",
            "vendor": "FastFreight Logistics",
            "amount": 4300.00,
            "due_date": now - timedelta(days=8),
            "status": "overdue",
            "description": "April express delivery — urgent parts",
            "created_at": now - timedelta(days=20),
        },
        {
            "invoice_number": "INV-008",
            "vendor": "TechParts Direct",
            "amount": 6100.00,
            "due_date": now - timedelta(days=5),
            "status": "overdue",
            "description": "Network switch and cabling",
            "created_at": now - timedelta(days=18),
        },
        {
            "invoice_number": "INV-009",
            "vendor": "Office Supplies Co",
            "amount": 2200.00,
            "due_date": now - timedelta(days=3),
            "status": "overdue",
            "description": "Printer cartridges and paper bulk order",
            "created_at": now - timedelta(days=12),
        },
        # PENDING
        {
            "invoice_number": "INV-010",
            "vendor": "CleanSpace Facilities",
            "amount": 1500.00,
            "due_date": now + timedelta(days=5),
            "status": "pending",
            "description": "Monthly office cleaning — April",
            "created_at": now - timedelta(days=3),
        },
        {
            "invoice_number": "INV-011",
            "vendor": "Office Supplies Co",
            "amount": 3200.00,
            "due_date": now + timedelta(days=8),
            "status": "pending",
            "description": "Q2 stationery and equipment",
            "created_at": now - timedelta(days=5),
        },
        {
            "invoice_number": "INV-012",
            "vendor": "Cloud Hosting Inc",
            "amount": 800.00,
            "due_date": now + timedelta(days=12),
            "status": "pending",
            "description": "Monthly server maintenance fee",
            "created_at": now - timedelta(days=2),
        },
        {
            "invoice_number": "INV-013",
            "vendor": "FastFreight Logistics",
            "amount": 5500.00,
            "due_date": now + timedelta(days=14),
            "status": "pending",
            "description": "Intercontinental freight — May batch",
            "created_at": now - timedelta(days=1),
        },
        {
            "invoice_number": "INV-014",
            "vendor": "TechParts Direct",
            "amount": 14000.00,
            "due_date": now + timedelta(days=18),
            "status": "pending",
            "description": "Workstation refresh — 10 units",
            "created_at": now,
        },
        {
            "invoice_number": "INV-015",
            "vendor": "CleanSpace Facilities",
            "amount": 950.00,
            "due_date": now + timedelta(days=20),
            "status": "pending",
            "description": "Deep clean — warehouse level B",
            "created_at": now,
        },
        {
            "invoice_number": "INV-016",
            "vendor": "Office Supplies Co",
            "amount": 1800.00,
            "due_date": now + timedelta(days=22),
            "status": "pending",
            "description": "Ergonomic chairs — finance team",
            "created_at": now,
        },
        {
            "invoice_number": "INV-017",
            "vendor": "Cloud Hosting Inc",
            "amount": 22000.00,
            "due_date": now + timedelta(days=25),
            "status": "pending",
            "description": "Annual enterprise SaaS license renewal",
            "created_at": now,
        },
        {
            "invoice_number": "INV-018",
            "vendor": "FastFreight Logistics",
            "amount": 3100.00,
            "due_date": now + timedelta(days=28),
            "status": "pending",
            "description": "Regional distribution run — Q2",
            "created_at": now,
        },
        {
            "invoice_number": "INV-019",
            "vendor": "TechParts Direct",
            "amount": 480.00,
            "due_date": now + timedelta(days=30),
            "status": "pending",
            "description": "Replacement keyboards and mice",
            "created_at": now,
        },
        {
            "invoice_number": "INV-020",
            "vendor": "CleanSpace Facilities",
            "amount": 2750.00,
            "due_date": now + timedelta(days=35),
            "status": "pending",
            "description": "Quarterly pest control — all floors",
            "created_at": now,
        },
    ])
    print("✅ Invoices seeded (20 total)")

    # ── PAYMENTS ───────────────────────────────────────────────────────────
    # 5 full payments for paid invoices + 3 partials on overdue ones
    await db.payments.insert_many([
        # Full payment — INV-001 ($5,000 wire)
        {
            "payment_id": "PMT-1",
            "invoice_id": "INV-001",
            "amount": 5000.00,
            "payment_date": now - timedelta(days=42),
            "payment_method": "wire",
            "reference_number": "WIRE-20260301-001",
            "notes": "Full settlement — Q1 office supplies",
            "created_at": now - timedelta(days=42),
        },
        # Full payment — INV-002 ($12,500 wire)
        {
            "payment_id": "PMT-2",
            "invoice_id": "INV-002",
            "amount": 12500.00,
            "payment_date": now - timedelta(days=32),
            "payment_method": "wire",
            "reference_number": "WIRE-20260310-002",
            "notes": "Annual cloud license — paid in full",
            "created_at": now - timedelta(days=32),
        },
        # Full payment — INV-003 ($3,800 check)
        {
            "payment_id": "PMT-3",
            "invoice_id": "INV-003",
            "amount": 3800.00,
            "payment_date": now - timedelta(days=27),
            "payment_method": "check",
            "reference_number": "CHK-00482",
            "notes": "March freight batch settlement",
            "created_at": now - timedelta(days=27),
        },
        # Full payment — INV-004 ($7,200 card)
        {
            "payment_id": "PMT-4",
            "invoice_id": "INV-004",
            "amount": 7200.00,
            "payment_date": now - timedelta(days=22),
            "payment_method": "card",
            "reference_number": "CARD-TXN-774821",
            "notes": "IT hardware — corporate card",
            "created_at": now - timedelta(days=22),
        },
        # Full payment — INV-005 ($1,500 wire)
        {
            "payment_id": "PMT-5",
            "invoice_id": "INV-005",
            "amount": 1500.00,
            "payment_date": now - timedelta(days=16),
            "payment_method": "wire",
            "reference_number": "WIRE-20260325-005",
            "notes": "Cleaning services March — cleared",
            "created_at": now - timedelta(days=16),
        },
        # Partial payment — INV-006 ($4,000 of $9,800 — still overdue)
        {
            "payment_id": "PMT-6",
            "invoice_id": "INV-006",
            "amount": 4000.00,
            "payment_date": now - timedelta(days=10),
            "payment_method": "wire",
            "reference_number": "WIRE-20260407-006",
            "notes": "Partial payment — remainder pending manager approval",
            "created_at": now - timedelta(days=10),
        },
        # Partial payment — INV-007 ($1,500 of $4,300 — still overdue)
        {
            "payment_id": "PMT-7",
            "invoice_id": "INV-007",
            "amount": 1500.00,
            "payment_date": now - timedelta(days=6),
            "payment_method": "check",
            "reference_number": "CHK-00491",
            "notes": "Partial — dispute on delivery surcharge ongoing",
            "created_at": now - timedelta(days=6),
        },
        # Partial payment — INV-008 ($2,000 of $6,100 — still overdue)
        {
            "payment_id": "PMT-8",
            "invoice_id": "INV-008",
            "amount": 2000.00,
            "payment_date": now - timedelta(days=4),
            "payment_method": "wire",
            "reference_number": "WIRE-20260413-008",
            "notes": "First installment — awaiting sign-off for balance",
            "created_at": now - timedelta(days=4),
        },
    ])
    print("✅ Payments seeded (8 transactions)")

    # ── AUDIT LOGS ─────────────────────────────────────────────────────────
    await db.audit_logs.insert_many([
        # Logins
        {
            "log_id": "LOG-001",
            "user_id": "admin@apcompass.com",
            "action": "login",
            "resource_type": "user",
            "resource_id": None,
            "details": "Admin login from 192.168.1.10",
            "timestamp": now - timedelta(days=60),
        },
        {
            "log_id": "LOG-002",
            "user_id": "emp1@apcompass.com",
            "action": "login",
            "resource_type": "user",
            "resource_id": None,
            "details": "Employee login from 192.168.1.22",
            "timestamp": now - timedelta(days=55),
        },
        # Invoice creation
        {
            "log_id": "LOG-003",
            "user_id": "emp1@apcompass.com",
            "action": "create_invoice",
            "resource_type": "invoice",
            "resource_id": "INV-001",
            "details": "Created invoice INV-001 for Office Supplies Co — $5,000.00",
            "timestamp": now - timedelta(days=60),
        },
        {
            "log_id": "LOG-004",
            "user_id": "emp2@apcompass.com",
            "action": "create_invoice",
            "resource_type": "invoice",
            "resource_id": "INV-002",
            "details": "Created invoice INV-002 for Cloud Hosting Inc — $12,500.00",
            "timestamp": now - timedelta(days=50),
        },
        {
            "log_id": "LOG-005",
            "user_id": "emp1@apcompass.com",
            "action": "create_invoice",
            "resource_type": "invoice",
            "resource_id": "INV-003",
            "details": "Created invoice INV-003 for FastFreight Logistics — $3,800.00",
            "timestamp": now - timedelta(days=45),
        },
        # Invoice approvals
        {
            "log_id": "LOG-006",
            "user_id": "manager@apcompass.com",
            "action": "approve_invoice",
            "resource_type": "invoice",
            "resource_id": "INV-001",
            "details": "Approved INV-001 — cleared for payment",
            "timestamp": now - timedelta(days=43),
        },
        {
            "log_id": "LOG-007",
            "user_id": "manager@apcompass.com",
            "action": "approve_invoice",
            "resource_type": "invoice",
            "resource_id": "INV-002",
            "details": "Approved INV-002 — annual license confirmed",
            "timestamp": now - timedelta(days=33),
        },
        {
            "log_id": "LOG-008",
            "user_id": "admin@apcompass.com",
            "action": "approve_invoice",
            "resource_type": "invoice",
            "resource_id": "INV-003",
            "details": "Approved INV-003 — freight batch verified",
            "timestamp": now - timedelta(days=28),
        },
        # Payments recorded
        {
            "log_id": "LOG-009",
            "user_id": "emp2@apcompass.com",
            "action": "record_payment",
            "resource_type": "payment",
            "resource_id": "INV-001",
            "details": "Recorded full payment $5,000.00 via wire — WIRE-20260301-001",
            "timestamp": now - timedelta(days=42),
        },
        {
            "log_id": "LOG-010",
            "user_id": "emp2@apcompass.com",
            "action": "record_payment",
            "resource_type": "payment",
            "resource_id": "INV-002",
            "details": "Recorded full payment $12,500.00 via wire — WIRE-20260310-002",
            "timestamp": now - timedelta(days=32),
        },
        {
            "log_id": "LOG-011",
            "user_id": "emp1@apcompass.com",
            "action": "record_payment",
            "resource_type": "payment",
            "resource_id": "INV-003",
            "details": "Recorded full payment $3,800.00 via check — CHK-00482",
            "timestamp": now - timedelta(days=27),
        },
        {
            "log_id": "LOG-012",
            "user_id": "emp1@apcompass.com",
            "action": "record_payment",
            "resource_type": "payment",
            "resource_id": "INV-006",
            "details": "Recorded partial payment $4,000.00 of $9,800.00 via wire",
            "timestamp": now - timedelta(days=10),
        },
        {
            "log_id": "LOG-013",
            "user_id": "emp2@apcompass.com",
            "action": "record_payment",
            "resource_type": "payment",
            "resource_id": "INV-007",
            "details": "Recorded partial payment $1,500.00 of $4,300.00 via check — dispute ongoing",
            "timestamp": now - timedelta(days=6),
        },
        # Overdue flags
        {
            "log_id": "LOG-014",
            "user_id": "system",
            "action": "flag_overdue",
            "resource_type": "invoice",
            "resource_id": "INV-006",
            "details": "Invoice INV-006 automatically flagged overdue — 12 days past due",
            "timestamp": now - timedelta(days=12),
        },
        {
            "log_id": "LOG-015",
            "user_id": "system",
            "action": "flag_overdue",
            "resource_type": "invoice",
            "resource_id": "INV-007",
            "details": "Invoice INV-007 automatically flagged overdue — 8 days past due",
            "timestamp": now - timedelta(days=8),
        },
        {
            "log_id": "LOG-016",
            "user_id": "system",
            "action": "flag_overdue",
            "resource_type": "invoice",
            "resource_id": "INV-008",
            "details": "Invoice INV-008 automatically flagged overdue — 5 days past due",
            "timestamp": now - timedelta(days=5),
        },
        {
            "log_id": "LOG-017",
            "user_id": "system",
            "action": "flag_overdue",
            "resource_type": "invoice",
            "resource_id": "INV-009",
            "details": "Invoice INV-009 automatically flagged overdue — 3 days past due",
            "timestamp": now - timedelta(days=3),
        },
        # Audit run by DeepSeek
        {
            "log_id": "LOG-018",
            "user_id": "admin@apcompass.com",
            "action": "run_audit",
            "resource_type": "system",
            "resource_id": None,
            "details": "Manual audit triggered — reviewed overdue invoice risk report",
            "timestamp": now - timedelta(days=2),
        },
        # User management
        {
            "log_id": "LOG-019",
            "user_id": "admin@apcompass.com",
            "action": "create_user",
            "resource_type": "user",
            "resource_id": "emp2@apcompass.com",
            "details": "Created new employee account for Carlos Rivera",
            "timestamp": now - timedelta(days=90),
        },
        {
            "log_id": "LOG-020",
            "user_id": "admin@apcompass.com",
            "action": "update_user_role",
            "resource_type": "user",
            "resource_id": "manager@apcompass.com",
            "details": "Promoted James Thornton from employee to manager",
            "timestamp": now - timedelta(days=45),
        },
    ])
    print("✅ Audit logs seeded (20 entries)")
    print("\n🎉 All done! Database is ready for demo.")
    client.close()

asyncio.run(seed())