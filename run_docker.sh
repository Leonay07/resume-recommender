#!/usr/bin/env bash

# Build and run the full stack via Docker.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${IMAGE_NAME:-resume-recommender}"
PORT="${PORT:-7860}"

echo "👉 Building Docker image '${IMAGE_NAME}'..."
docker build -t "${IMAGE_NAME}" "$ROOT_DIR"
echo "✅ Build completed."

if [ ! -f "$ROOT_DIR/backend/.env" ]; then
  echo "⚠️  未找到 backend/.env，容器会缺少 RAPID_API_KEY/RAPID_API_HOST。"
fi

echo "👉 Starting container on port ${PORT}..."
docker run --rm -p "${PORT}:7860" --env-file "$ROOT_DIR/backend/.env" "${IMAGE_NAME}"
