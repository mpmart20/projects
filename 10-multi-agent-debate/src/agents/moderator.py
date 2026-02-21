"""Moderator agent that facilitates the debate."""
import os, anthropic
from .base import AgentMessage
from dotenv import load_dotenv

load_dotenv()

class ModeratorAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def synthesize(self, topic: str, messages: list[AgentMessage]) -> str:
        debate_text = "\n".join([f"{m.agent_name} ({m.role}): {m.content}" for m in messages])
        msg = self.client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=500,
            system="You are a debate moderator. Synthesize the key arguments fairly.",
            messages=[{
                "role": "user",
                "content": f"Synthesize the main points from this debate on: {topic}\n\n{debate_text}"
            }]
        )
        return msg.content[0].text
