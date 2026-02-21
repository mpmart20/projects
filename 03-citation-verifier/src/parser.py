"""Extracts factual claims from AI-generated text."""
import os, json, anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaimParser:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def extract_claims(self, text: str) -> list[dict]:
        msg = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            system="Extract factual claims that can be verified. Return JSON only.",
            messages=[{
                "role": "user",
                "content": f"""Extract all verifiable factual claims from this text.
Return JSON array: [{{"claim": "...", "type": "statistic|fact|quote|date", "confidence": 0-1}}]

Text: {text}"""
            }]
        )
        try:
            text_response = msg.content[0].text.strip()
            if "```" in text_response:
                text_response = text_response.split("```")[1].replace("json", "").strip()
            return json.loads(text_response)
        except:
            return []
