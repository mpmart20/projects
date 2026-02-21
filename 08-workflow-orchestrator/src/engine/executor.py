"""Workflow execution engine."""
import json, time
from .state import WorkflowState
from ..tools.base import ToolRegistry

class WorkflowExecutor:
    def __init__(self, tools: ToolRegistry = None):
        self.tools = tools or ToolRegistry()
        self.state = WorkflowState()

    def execute(self, workflow: dict) -> dict:
        self.state.initialize(workflow)
        results = []

        for step in workflow.get("steps", []):
            print(f"  Executing step: {step['name']}")
            try:
                result = self._execute_step(step)
                results.append({"step": step["name"], "status": "success", "output": result})
                self.state.update(step["name"], result)
            except Exception as e:
                results.append({"step": step["name"], "status": "error", "error": str(e)})
                if not step.get("continue_on_error", False):
                    break
            time.sleep(0.1)

        return {"workflow": workflow["name"], "results": results, "state": self.state.get_all()}

    def _execute_step(self, step: dict):
        tool_name = step.get("tool")
        if tool_name and tool_name in self.tools:
            return self.tools.run(tool_name, step.get("params", {}))
        return {"placeholder": f"Step {step['name']} completed"}
