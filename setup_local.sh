#!/usr/bin/env bash

# One-click local environment bootstrapper.
# - Creates a Python virtualenv under backend/.venv and installs requirements
# - Installs frontend npm dependencies

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="$ROOT_DIR/backend/.venv"

echo "👉 Setting up backend virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$ROOT_DIR/backend/requirements.txt"
deactivate
echo "✅ Backend dependencies installed."

echo "👉 Installing frontend dependencies..."
cd "$ROOT_DIR/frontend"
npm install
echo "✅ Frontend dependencies installed."

echo ""
echo "All set! Start backend with 'source backend/.venv/bin/activate && uvicorn app:app --reload'"
echo "and frontend with 'npm run dev' from the frontend directory."
