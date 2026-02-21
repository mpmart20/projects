"""Base agent class for debate participants."""
import os, anthropic
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AgentMessage:
    agent_name: str
    role: str
    content: str
    round: int
    citations: list[str] = field(default_factory=list)

class BaseAgent:
    def __init__(self, name: str, perspective: str, model: str = "claude-haiku-4-5-20251001"):
        self.name = name
        self.perspective = perspective
        self.model = model
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
        self.message_history = []

    def respond(self, topic: str, previous_messages: list[AgentMessage], round_num: int) -> AgentMessage:
        context = "\n".join([f"{m.agent_name}: {m.content}" for m in previous_messages[-4:]])
        system = f"""You are {self.name}, a debater with a {self.perspective} perspective.
Engage thoughtfully with other arguments. Be specific, cite reasoning, and stay on topic.
Always identify 1-2 key points to argue and directly respond to previous arguments."""

        prompt = f"Topic: {topic}\n\nDebate so far:\n{context}\n\nYour turn to argue from a {self.perspective} perspective (2-3 sentences):"

        msg = self.client.messages.create(
            model=self.model, max_tokens=300, system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return AgentMessage(
            agent_name=self.name, role=self.perspective,
            content=msg.content[0].text, round=round_num
        )
