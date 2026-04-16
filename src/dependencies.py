import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/ap_ar_db")

# Validate required keys (only warn for now)
if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY.startswith("your_"):
    print("Warning: ANTHROPIC_API_KEY not properly set")

if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("your_"):
    print("Warning: DEEPSEEK_API_KEY not properly set")
