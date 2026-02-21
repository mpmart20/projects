# Multi-Agent Debate System

Multiple AI agents with distinct perspectives debate complex questions and converge on reasoned conclusions.

## Setup

```bash
# Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run development servers
cd backend && uvicorn main:app --reload
cd frontend && npm run dev
```

## Tech Stack
- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI
- **AI**: Anthropic Claude API

## Project Status
🚧 In Development
