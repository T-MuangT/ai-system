import os
import re
from pydantic_ai import Agent
from src.dependencies import ANTHROPIC_API_KEY

os.environ['ANTHROPIC_API_KEY'] = ANTHROPIC_API_KEY

# Claude's system prompt — knows it can delegate to DeepSeek
CLAUDE_SYSTEM_PROMPT = """You are a professional AP/AR Assistant for AP Compass, a finance operations platform.

You help users with:
- Invoice status, approvals, and overdue items
- Payment tracking and history
- Financial summaries and cashflow
- Audit log review
- Vendor and supplier queries

You have a DeepSeek financial auditor agent available to you. When a user asks about:
- Specific invoice data or lists ("show me overdue invoices", "what invoices are pending")
- Payment details ("what payments were made", "show payments for INV-001")
- Financial analysis ("summarize cashflow", "audit report", "risk assessment")
- Database updates ("mark INV-006 as paid", "approve invoice INV-003")
- Audit logs ("what actions were taken", "who approved invoices")

...respond with exactly this format to trigger DeepSeek:
[DELEGATE_TO_DEEPSEEK: <your specific task instruction for DeepSeek>]

For general questions, greetings, or explanations that don't need live data, answer directly yourself.

After receiving DeepSeek's analysis, summarize it clearly and conversationally for the user.
"""

claude_agent = Agent(
    'anthropic:claude-sonnet-4-5',
    system_prompt=CLAUDE_SYSTEM_PROMPT,
)


class AssistantAgent:
    def __init__(self, auditor_agent=None):
        self.auditor = auditor_agent  # DeepSeek AuditorAgent injected at startup

    def set_auditor(self, auditor_agent):
        self.auditor = auditor_agent

    async def run(self, message: str) -> str:
        try:
            # Step 1: Claude decides what to do
            result = await claude_agent.run(message)
            claude_response = result.output if hasattr(result, 'output') else str(result)

            # Step 2: Check if Claude wants to delegate to DeepSeek
            delegate_match = re.search(
                r'\[DELEGATE_TO_DEEPSEEK:\s*(.+?)\]',
                claude_response,
                re.DOTALL
            )

            if delegate_match and self.auditor:
                deepseek_task = delegate_match.group(1).strip()

                # Step 3: DeepSeek fetches/writes real data using its tools
                deepseek_result = await self.auditor.run(deepseek_task)

                # Step 4: Claude synthesizes DeepSeek's findings into a user-friendly reply
                synthesis_prompt = (
                    f"The user asked: {message}\n\n"
                    f"Your financial auditor (DeepSeek) retrieved this data and analysis:\n\n"
                    f"{deepseek_result}\n\n"
                    f"Please summarize this clearly and conversationally for the user. "
                    f"Highlight any important findings, risks, or action items."
                )
                final_result = await claude_agent.run(synthesis_prompt)
                return final_result.output if hasattr(final_result, 'output') else str(final_result)

            # No delegation needed — return Claude's direct answer
            return claude_response

        except Exception as e:
            return f"Assistant Error: {str(e)}"