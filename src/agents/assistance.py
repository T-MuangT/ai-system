from pydantic_ai import Agent
from src.dependencies import ANTHROPIC_API_KEY
import os

# 1. Set the environment variable so PydanticAI can find your key automatically
os.environ['ANTHROPIC_API_KEY'] = ANTHROPIC_API_KEY

# 2. Define the Agent once at the top level
# PydanticAI handles the 'client', 'messages', and 'max_tokens' for you
assistant_agent = Agent(
    'anthropic:claude-sonnet-4-5',
    system_prompt="You are a professional AR/AP Assistant. Help users with invoice queries.",
)

# 3. Use a simple class or function to wrap the 'run' call
class AssistantAgent:
    async def run(self, message: str):
        try:
            # We use the assistant_agent we defined above
            # result.data will contain the clean text response
            result = await assistant_agent.run(message)
            return result.output
        except Exception as e:
            return f"Claude API Error: {str(e)}"