"""Workflow state management."""

class WorkflowState:
    def __init__(self):
        self._state = {}

    def initialize(self, workflow: dict):
        self._state = {"workflow_name": workflow["name"], "started_at": __import__("time").time(), "variables": {}}

    def update(self, step_name: str, result):
        self._state["variables"][step_name] = result

    def get(self, key: str):
        return self._state.get(key)

    def get_all(self) -> dict:
        return self._state.copy()
