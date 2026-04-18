import openai
import json
from src.dependencies import DEEPSEEK_API_KEY
from motor.motor_asyncio import AsyncIOMotorClient
from src.dependencies import MONGODB_URL

# Database tools DeepSeek can call
DB_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_invoices",
            "description": "Retrieve invoices from the database. Can filter by status (pending, paid, overdue) or vendor name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by invoice status: 'pending', 'paid', or 'overdue'. Leave empty for all.",
                        "enum": ["pending", "paid", "overdue", "all"]
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Filter by vendor name (partial match). Leave empty for all vendors."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_payments",
            "description": "Retrieve payment transactions from the database. Can filter by invoice ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "invoice_id": {
                        "type": "string",
                        "description": "Filter payments by invoice ID (e.g. INV-001). Leave empty for all payments."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_audit_logs",
            "description": "Retrieve audit log entries. Can filter by action type or user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Filter by action type e.g. 'approve_invoice', 'record_payment', 'flag_overdue'."
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Filter by user email who performed the action."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_invoice_status",
            "description": "Update the status of an invoice. Use this to mark invoices as paid, approved, or overdue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "invoice_number": {
                        "type": "string",
                        "description": "The invoice number to update e.g. 'INV-001'."
                    },
                    "new_status": {
                        "type": "string",
                        "description": "The new status to set.",
                        "enum": ["pending", "paid", "overdue", "approved"]
                    }
                },
                "required": ["invoice_number", "new_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_summary_stats",
            "description": "Get a high-level financial summary: total invoices, paid count, overdue count, total amounts.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


async def _execute_tool(tool_name: str, args: dict) -> str:
    """Execute a database tool call and return result as JSON string."""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client["ap_ar_db"]

    try:
        if tool_name == "get_invoices":
            query = {}
            if args.get("status") and args["status"] != "all":
                query["status"] = args["status"]
            if args.get("vendor"):
                query["vendor"] = {"$regex": args["vendor"], "$options": "i"}
            invoices = await db.invoices.find(query).to_list(length=100)
            for inv in invoices:
                inv["_id"] = str(inv["_id"])
                if "due_date" in inv and inv["due_date"]:
                    inv["due_date"] = str(inv["due_date"])
                if "created_at" in inv and inv["created_at"]:
                    inv["created_at"] = str(inv["created_at"])
            return json.dumps(invoices)

        elif tool_name == "get_payments":
            query = {}
            if args.get("invoice_id"):
                query["invoice_id"] = args["invoice_id"]
            payments = await db.payments.find(query).to_list(length=100)
            for pay in payments:
                pay["_id"] = str(pay["_id"])
                if "payment_date" in pay and pay["payment_date"]:
                    pay["payment_date"] = str(pay["payment_date"])
                if "created_at" in pay and pay["created_at"]:
                    pay["created_at"] = str(pay["created_at"])
            return json.dumps(payments)

        elif tool_name == "get_audit_logs":
            query = {}
            if args.get("action"):
                query["action"] = args["action"]
            if args.get("user_id"):
                query["user_id"] = args["user_id"]
            logs = await db.audit_logs.find(query).to_list(length=100)
            for log in logs:
                log["_id"] = str(log["_id"])
                if "timestamp" in log and log["timestamp"]:
                    log["timestamp"] = str(log["timestamp"])
            return json.dumps(logs)

        elif tool_name == "update_invoice_status":
            invoice_number = args["invoice_number"]
            new_status = args["new_status"]
            result = await db.invoices.update_one(
                {"invoice_number": invoice_number},
                {"$set": {"status": new_status}}
            )
            if result.matched_count == 0:
                return json.dumps({"error": f"Invoice {invoice_number} not found"})
            # Log the update
            await db.audit_logs.insert_one({
                "log_id": f"LOG-AUTO-{invoice_number}-{new_status}",
                "user_id": "deepseek-auditor",
                "action": "update_invoice_status",
                "resource_type": "invoice",
                "resource_id": invoice_number,
                "details": f"DeepSeek updated {invoice_number} status to '{new_status}'",
                "timestamp": __import__("datetime").datetime.utcnow()
            })
            return json.dumps({"success": True, "invoice": invoice_number, "new_status": new_status})

        elif tool_name == "get_summary_stats":
            total = await db.invoices.count_documents({})
            paid = await db.invoices.count_documents({"status": "paid"})
            overdue = await db.invoices.count_documents({"status": "overdue"})
            pending = await db.invoices.count_documents({"status": "pending"})

            paid_invoices = await db.invoices.find({"status": "paid"}).to_list(length=100)
            overdue_invoices = await db.invoices.find({"status": "overdue"}).to_list(length=100)
            total_paid_amount = sum(inv.get("amount", 0) for inv in paid_invoices)
            total_overdue_amount = sum(inv.get("amount", 0) for inv in overdue_invoices)

            return json.dumps({
                "total_invoices": total,
                "paid_count": paid,
                "overdue_count": overdue,
                "pending_count": pending,
                "total_paid_amount": total_paid_amount,
                "total_overdue_amount": total_overdue_amount,
                "net_cashflow": total_paid_amount - total_overdue_amount
            })

        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})

    finally:
        client.close()


class AuditorAgent:
    def __init__(self):
        if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("your_"):
            raise ValueError("DEEPSEEK_API_KEY is required and must be properly set")
        self.client = openai.AsyncOpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )

    async def run(self, task: str) -> str:
        """
        Run DeepSeek with database tool access.
        DeepSeek will call tools as needed, then return a final analysis.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a financial auditor AI with direct access to the AP/AR database. "
                    "When asked about invoices, payments, or financial data, always use your tools "
                    "to fetch real data before answering. You can also update invoice statuses when instructed. "
                    "Be concise, factual, and highlight any risks or anomalies you find."
                )
            },
            {"role": "user", "content": task}
        ]

        # Agentic loop — DeepSeek can call multiple tools before giving final answer
        for _ in range(5):  # max 5 tool call rounds
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=DB_TOOLS,
                tool_choice="auto",
                max_tokens=1500
            )

            message = response.choices[0].message

            # If no tool calls, we have the final answer
            if not message.tool_calls:
                return message.content

            # Execute each tool call DeepSeek requested
            messages.append(message)  # add assistant message with tool_calls

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    args = {}

                result = await _execute_tool(tool_name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return "DeepSeek reached maximum tool call rounds without a final answer."