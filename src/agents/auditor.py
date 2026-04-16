import openai
from src.dependencies import DEEPSEEK_API_KEY

class AuditorAgent:
    def __init__(self):
        if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("your_"):
            raise ValueError("DEEPSEEK_API_KEY is required and must be properly set")
        self.client = openai.AsyncOpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )

    async def run(self, task: str):
        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are an auditor AI that analyzes financial data and provides insights."},
                    {"role": "user", "content": task}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"DeepSeek API Error: {str(e)}"

auditor_agent = None
