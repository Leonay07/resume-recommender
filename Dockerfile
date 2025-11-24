# ============================
# 1. Build Frontend (Vite)
# ============================
FROM node:18 AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
COPY frontend/ ./

RUN npm install
RUN npm run build   # output → /app/frontend/dist


# ============================
# 2. Build Backend (FastAPI)
# ============================
FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build → backend/static
COPY --from=frontend-builder /app/frontend/dist ./backend/static


# ============================
# 3. Expose + Run API
# ============================
EXPOSE 7860

WORKDIR /app/backend

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
