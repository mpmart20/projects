"""Importance ranking for content chunks."""
import os, json, anthropic
from dotenv import load_dotenv

load_dotenv()

class ContentRanker:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def rank_chunks(self, chunks: list[dict], query: str = "") -> list[dict]:
        ranked = []
        for chunk in chunks:
            score = self._score_chunk(chunk["text"], query)
            ranked.append({**chunk, "importance": score})
        return sorted(ranked, key=lambda x: x["importance"], reverse=True)

    def _score_chunk(self, text: str, query: str) -> float:
        msg = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": f"Rate the importance of this text (0.0-1.0) for: '{query}'\nText: {text[:500]}\nReturn only a decimal number."
            }]
        )
        try:
            return float(msg.content[0].text.strip())
        except:
            return 0.5
