#!/usr/bin/env bash

# One-click local environment bootstrapper.
# - Installs Python dependencies via Poetry
# - Installs frontend npm dependencies

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POETRY_BIN="${POETRY_BIN:-poetry}"

if ! command -v "$POETRY_BIN" >/dev/null 2>&1; then
  echo "❌ Poetry is not installed. Please install Poetry and rerun this script."
  exit 1
fi

echo "👉 Installing backend dependencies with Poetry..."
cd "$ROOT_DIR"
"$POETRY_BIN" install --with dev
echo "✅ Backend dependencies installed."

echo "👉 Installing frontend dependencies..."
cd "$ROOT_DIR/frontend"
npm install
echo "✅ Frontend dependencies installed."

echo ""
echo "All set! Start backend with 'poetry run uvicorn backend.app:app --reload'"
echo "and frontend with 'npm run dev' from the frontend directory."
