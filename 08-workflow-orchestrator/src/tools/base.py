"""Tool registry and base class."""
from abc import ABC, abstractmethod

class BaseTool(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def run(self, params: dict) -> dict:
        pass

class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def run(self, name: str, params: dict) -> dict:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not registered")
        return self._tools[name].run(params)
