"""Scores prompt quality using Claude as a judge."""
import os, anthropic, json
from dotenv import load_dotenv

load_dotenv()

class PromptEvaluator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    def score(self, prompt: str, goal: str) -> dict:
        msg = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system='You are a prompt quality evaluator. Return only JSON with scores 0-10.',
            messages=[{
                "role": "user",
                "content": f"""Score this prompt for achieving the goal.
Goal: {goal}
Prompt: {prompt}

Return JSON: {{"clarity": 0-10, "specificity": 0-10, "effectiveness": 0-10, "overall": 0-10}}"""
            }]
        )
        try:
            text = msg.content[0].text.strip()
            if "```" in text:
                text = text.split("```")[1].replace("json", "").strip()
            return json.loads(text)
        except:
            return {"clarity": 5, "specificity": 5, "effectiveness": 5, "overall": 5}
