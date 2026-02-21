# AI Portfolio — Anthropic-Aligned Projects

10 production-quality AI projects demonstrating safety, evaluation, and agentic systems.

## Projects

| # | Project | Focus | Difficulty |
|---|---------|-------|------------|
| 1 | [Constitutional AI Playground](./01-constitutional-ai-playground) | AI Safety | ⭐ |
| 2 | [Prompt Optimization Tool](./02-prompt-optimizer) | Evaluation | ⭐⭐ |
| 3 | [Citation Verification System](./03-citation-verifier) | Factuality | ⭐⭐ |
| 4 | [Multi-Model Comparator](./04-model-comparator) | Benchmarking | ⭐⭐ |
| 5 | [Context Window Optimizer](./05-context-optimizer) | Efficiency | ⭐⭐⭐ |
| 6 | [AI Safety Testing Framework](./06-safety-tester) | Red-teaming | ⭐⭐⭐ |
| 7 | [RAG Evaluator](./07-rag-evaluator) | Retrieval | ⭐⭐⭐ |
| 8 | [Workflow Orchestrator](./08-workflow-orchestrator) | Agents | ⭐⭐⭐⭐ |
| 9 | [Interpretability Dashboard](./09-interpretability-dashboard) | Safety Research | ⭐⭐⭐⭐ |
| 10 | [Multi-Agent Debate System](./10-multi-agent-debate) | Multi-Agent | ⭐⭐⭐⭐⭐ |

## Quick Start

```bash
# 1. Set your API key in any project
cp 01-constitutional-ai-playground/.env .env
# Edit .env: ANTHROPIC_API_KEY=your_key_here

# 2. Run a project
cd 01-constitutional-ai-playground/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Tech Stack
- Python 3.11 + FastAPI + Pydantic
- React 18 + TypeScript + Vite
- Anthropic Claude API
- ChromaDB for vector storage
