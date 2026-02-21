#!/bin/bash
# Run any project by number
# Usage: ./run_project.sh 1

PROJECT=$1
DIRS=(
  "" # placeholder for 0
  "01-constitutional-ai-playground"
  "02-prompt-optimizer"
  "03-citation-verifier"
  "04-model-comparator"
  "05-context-optimizer"
  "06-safety-tester"
  "07-rag-evaluator"
  "08-workflow-orchestrator"
  "09-interpretability-dashboard"
  "10-multi-agent-debate"
)

if [ -z "$PROJECT" ] || [ "$PROJECT" -lt 1 ] || [ "$PROJECT" -gt 10 ]; then
  echo "Usage: ./run_project.sh <1-10>"
  exit 1
fi

DIR="${DIRS[$PROJECT]}"
echo "Starting Project $PROJECT: $DIR"
cd "$HOME/ai-portfolio/$DIR"

# Check for backend
if [ -f "backend/requirements.txt" ]; then
  echo "Starting backend..."
  cd backend
  pip install -r requirements.txt -q
  uvicorn main:app --reload --port $((8000 + PROJECT)) &
  cd ..
fi

# Check for CLI
if [ -f "src/cli.py" ] || [ -f "src/runner.py" ]; then
  echo "To run CLI:"
  echo "  cd $HOME/ai-portfolio/$DIR"
  echo "  pip install -r requirements.txt"
  echo "  python src/cli.py --help"
fi
