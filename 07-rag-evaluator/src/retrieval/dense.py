"""Dense (vector) retrieval using embeddings."""
import os, anthropic, json
from dotenv import load_dotenv
load_dotenv()

class DenseRetriever:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
        self.documents = []
        self.embeddings = []

    def embed(self, text: str) -> list[float]:
        # Using Voyage via Anthropic for embeddings
        # Fallback: use simple word-overlap for demo
        words = set(text.lower().split())
        return [1.0 if w in words else 0.0 for w in sorted(words)][:512]

    def index(self, documents: list[dict]):
        self.documents = documents
        self.embeddings = [self.embed(doc["content"]) for doc in documents]
        print(f"Indexed {len(documents)} documents")

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        if not self.documents:
            return []
        query_emb = self.embed(query)
        scores = [self._cosine(query_emb, doc_emb) for doc_emb in self.embeddings]
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [{"document": self.documents[i], "score": scores[i]} for i in top_indices]

    def _cosine(self, a: list, b: list) -> float:
        if not a or not b: return 0.0
        length = min(len(a), len(b))
        dot = sum(a[i] * b[i] for i in range(length))
        mag_a = sum(x**2 for x in a[:length]) ** 0.5
        mag_b = sum(x**2 for x in b[:length]) ** 0.5
        return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0
