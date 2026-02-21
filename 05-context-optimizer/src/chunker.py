"""Text chunking strategies."""
import re

class TextChunker:
    def chunk(self, text: str, max_tokens: int = 1000, overlap: int = 100) -> list[dict]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + max_tokens, len(words))
            chunk_words = words[start:end]
            chunks.append({
                "text": " ".join(chunk_words),
                "start": start,
                "end": end,
                "token_count": len(chunk_words)
            })
            start += max_tokens - overlap
        return chunks
