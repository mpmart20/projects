"""Claude model client."""
import os, time, anthropic
from base import BaseModel, ModelResponse
from dotenv import load_dotenv

load_dotenv()

CLAUDE_PRICING = {
    "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5-20251001":  {"input": 0.25, "output": 1.25},
}

class ClaudeModel(BaseModel):
    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        self.model = model
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def complete(self, prompt: str, system: str = "") -> ModelResponse:
        start = time.time()
        kwargs = {"model": self.model, "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]}
        if system:
            kwargs["system"] = system
        msg = self.client.messages.create(**kwargs)
        latency = (time.time() - start) * 1000
        pricing = CLAUDE_PRICING.get(self.model, {"input": 3.00, "output": 15.00})
        cost = (msg.usage.input_tokens / 1_000_000 * pricing["input"] +
                msg.usage.output_tokens / 1_000_000 * pricing["output"])
        return ModelResponse(
            model_name=self.model,
            content=msg.content[0].text,
            input_tokens=msg.usage.input_tokens,
            output_tokens=msg.usage.output_tokens,
            latency_ms=latency,
            cost_usd=cost
        )
