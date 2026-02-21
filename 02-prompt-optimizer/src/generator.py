"""Generates prompt variations using Claude."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic
from dotenv import load_dotenv

load_dotenv()

VARIATION_TYPES = [
    "more concise", "more detailed", "use examples", "use step-by-step format",
    "more formal tone", "more conversational tone", "add context", "use bullet points",
    "reframe as a question", "add role assignment",
]

class PromptGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def generate(self, base_prompt: str, goal: str, count: int = 10) -> list[str]:
        variations = [base_prompt]  # always include original
        selected_types = VARIATION_TYPES[:min(count - 1, len(VARIATION_TYPES))]

        for variation_type in selected_types:
            msg = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system="You are a prompt engineering expert. Rewrite prompts to improve them.",
                messages=[{
                    "role": "user",
                    "content": f"Rewrite this prompt to be {variation_type}. Return ONLY the rewritten prompt, nothing else.\n\nOriginal: {base_prompt}\nGoal: {goal}"
                }]
            )
            variations.append(msg.content[0].text.strip())

        return variations[:count]
