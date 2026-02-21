"""File-based caching to avoid redundant API calls."""
import json, hashlib, os
from pathlib import Path

class Cache:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _key(self, value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    def get(self, prompt: str):
        path = self.cache_dir / f"{self._key(prompt)}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    def set(self, prompt: str, data: dict):
        path = self.cache_dir / f"{self._key(prompt)}.json"
        path.write_text(json.dumps(data, indent=2))
