# Constitutional AI Playground

Interactively explore how constitutional rules shape AI behavior.

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
