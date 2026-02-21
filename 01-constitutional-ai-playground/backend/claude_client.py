"""Shared Claude API client used across all projects."""
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

def get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        raise ValueError("ANTHROPIC_API_KEY not set in .env file")
    return anthropic.Anthropic(api_key=api_key)

def chat(prompt: str, system: str = "", model: str = "claude-sonnet-4-5-20250929") -> str:
    client = get_client()
    kwargs = {"model": model, "max_tokens": 2048, "messages": [{"role": "user", "content": prompt}]}
    if system:
        kwargs["system"] = system
    message = client.messages.create(**kwargs)
    return message.content[0].text
