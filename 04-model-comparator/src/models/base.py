"""Abstract base class for all model clients."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time

@dataclass
class ModelResponse:
    model_name: str
    content: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float

class BaseModel(ABC):
    @abstractmethod
    def complete(self, prompt: str, system: str = "") -> ModelResponse:
        pass
