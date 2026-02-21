"""Tests model behavior across diverse inputs."""
import os, json, anthropic
from dotenv import load_dotenv

load_dotenv()

BEHAVIOR_TESTS = {
    "consistency": [
        {"q": "Is the sky blue?", "variations": ["Is the sky blue?", "What color is the sky?", "The sky is what color?"]},
    ],
    "reasoning": [
        {"q": "What is 2+2?", "variations": ["What is 2+2?", "Calculate 2 plus 2", "If I have 2 apples and add 2, how many?"]},
    ]
}

class BehaviorExperimenter:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def run_consistency_test(self, questions: list[str]) -> dict:
        responses = []
        for q in questions:
            msg = self.client.messages.create(
                model="claude-haiku-4-5-20251001", max_tokens=200,
                messages=[{"role": "user", "content": q}]
            )
            responses.append({"question": q, "response": msg.content[0].text})

        # Score consistency (simplified: check if responses are similar length)
        lengths = [len(r["response"]) for r in responses]
        variance = (max(lengths) - min(lengths)) / max(lengths) if lengths else 0
        consistency_score = 1 - variance

        return {"responses": responses, "consistency_score": consistency_score}
