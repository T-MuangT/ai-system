# AP-AR AI Backend

A FastAPI backend for Accounts Payable/Receivable management with AI-powered chat (Claude) and auditing (DeepSeek).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get API keys:
   - **Claude (Anthropic)**: Sign up at [Anthropic Console](https://console.anthropic.com/) and get your API key
   - **DeepSeek**: Sign up at [DeepSeek Platform](https://platform.deepseek.com/) and get your API key

3. Set up environment variables in `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   DEEPSEEK_API_KEY=sk-...
   MONGODB_URL=mongodb://localhost:27017/ap_ar_db
   ```

4. Set up MongoDB:
   - Install MongoDB locally or use MongoDB Atlas
   - Update MONGODB_URL if needed

5. Run the server:
   ```bash
   python run.py
   ```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /users/me` - Get current user profile

### Dashboard
- `GET /dashboard/summary` - Invoice statistics

### Invoices
- `GET /invoices` - List all invoices
- `POST /invoices` - Create new invoice
- `GET /invoices/{id}` - Get specific invoice
- `PUT /invoices/{id}` - Update invoice
- `POST /invoices/{id}/approve` - Approve invoice
- `POST /invoices/{id}/payments` - Record payment

### AI Features
- `POST /chat` - Chat with Claude AI
- `GET /chat/{user_id}` - Get chat history
- `POST /audit` - Run audit with DeepSeek AI

### Data Management
- `GET /users` - List users
- `POST /users` - Create user
- `GET /customers` - List customers
- `POST /customers` - Create customer
- `GET /vendors` - List vendors
- `POST /vendors` - Create vendor
- `GET /payments` - List payments
- `GET /reports` - List reports
- `POST /reports` - Create report
- `GET /audit-logs` - List audit logs

## Architecture

- **Chat Assistant**: Claude (Anthropic) for conversational AI
- **Auditor**: DeepSeek for financial analysis and auditing
- **Database**: MongoDB with Beanie ODM
- **API**: FastAPI with automatic OpenAPI docs at http://localhost:8000/docs

## Frontend Integration

The backend is fully integrated with the React frontend running on `http://localhost:5173`. All API endpoints match the frontend's service calls, and CORS is configured for seamless communication.