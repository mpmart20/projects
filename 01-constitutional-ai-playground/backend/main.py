"""Constitutional AI Playground - FastAPI Backend"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import anthropic, os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Constitutional AI Playground")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

class Rule(BaseModel):
    id: str
    name: str
    description: str
    enabled: bool = True

class TestRequest(BaseModel):
    prompt: str
    rules: list[Rule]
    model: str = "claude-sonnet-4-5-20250929"

class TestResponse(BaseModel):
    unconstrained: str
    constrained: str
    rules_triggered: list[str]

def build_constitution(rules: list[Rule]) -> str:
    active = [r for r in rules if r.enabled]
    if not active:
        return ""
    lines = ["You must follow these constitutional principles:\n"]
    for i, rule in enumerate(active, 1):
        lines.append(f"{i}. {rule.name}: {rule.description}")
    return "\n".join(lines)

@app.post("/api/test", response_model=TestResponse)
async def test_prompt(req: TestRequest):
    # Unconstrained response
    unconstrained_msg = client.messages.create(
        model=req.model,
        max_tokens=1024,
        messages=[{"role": "user", "content": req.prompt}]
    )
    unconstrained = unconstrained_msg.content[0].text

    # Constrained response
    constitution = build_constitution(req.rules)
    constrained_msg = client.messages.create(
        model=req.model,
        max_tokens=1024,
        system=constitution,
        messages=[{"role": "user", "content": req.prompt}]
    )
    constrained = constrained_msg.content[0].text

    # Detect which rules may have been triggered (simplified heuristic)
    rules_triggered = []
    for rule in req.rules:
        if rule.enabled and len(constrained) != len(unconstrained):
            rules_triggered.append(rule.id)

    return TestResponse(
        unconstrained=unconstrained,
        constrained=constrained,
        rules_triggered=rules_triggered
    )

@app.get("/api/health")
async def health():
    return {"status": "ok"}
