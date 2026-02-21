"""Context compression strategies."""
import os, anthropic
from chunker import TextChunker
from ranker import ContentRanker
from dotenv import load_dotenv

load_dotenv()

class ContextCompressor:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
        self.chunker = TextChunker()
        self.ranker = ContentRanker()

    def compress(self, text: str, target_tokens: int, query: str = "") -> dict:
        original_tokens = len(text.split())
        if original_tokens <= target_tokens:
            return {"compressed": text, "original_tokens": original_tokens, "compressed_tokens": original_tokens, "ratio": 1.0}

        chunks = self.chunker.chunk(text)
        ranked = self.ranker.rank_chunks(chunks, query)

        # Keep top chunks until we hit target
        selected, total = [], 0
        for chunk in ranked:
            if total + chunk["token_count"] <= target_tokens:
                selected.append(chunk)
                total += chunk["token_count"]

        selected.sort(key=lambda x: x["start"])
        compressed = " ... ".join(c["text"] for c in selected)
        compressed_tokens = len(compressed.split())

        return {
            "compressed": compressed,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "ratio": compressed_tokens / original_tokens,
            "chunks_kept": len(selected),
            "chunks_total": len(chunks)
        }
