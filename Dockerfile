# ============================
# 1. Build Frontend (Vite)
# ============================
FROM node:18 AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build   # output → /app/frontend/dist


# ============================
# 2. Build Backend (FastAPI)
# ============================
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly (mirrors pyproject requirements)
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    requests \
    python-dotenv \
    python-multipart \
    pdfplumber \
    python-docx \
    scikit-learn

# Copy backend code
COPY backend ./backend
RUN mkdir -p backend/static

# Copy frontend build → backend/static
COPY --from=frontend-builder /app/frontend/dist ./backend/static

# ============================
# 3. Expose + Run API
# ============================
EXPOSE 7860

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]
