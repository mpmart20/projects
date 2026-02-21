"""Scores claim verifiability using web search simulation."""
import os, json, anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaimScorer:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def score(self, claim: str) -> dict:
        msg = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system="You are a fact-checker. Evaluate claims based on your knowledge.",
            messages=[{
                "role": "user",
                "content": f"""Evaluate this claim: "{claim}"

Return JSON:
{{
  "status": "verified|unverified|conflicting",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation",
  "evidence": ["supporting point 1", "supporting point 2"],
  "sources": ["Wikipedia", "Common knowledge"]
}}"""
            }]
        )
        try:
            text = msg.content[0].text.strip()
            if "```" in text:
                text = text.split("```")[1].replace("json", "").strip()
            return json.loads(text)
        except:
            return {"status": "unverified", "confidence": 0.5, "reasoning": "Could not parse", "evidence": [], "sources": []}
