# Docker Compose Stack

This page describes the local microservice deployment that mirrors the cloud-grade
architecture: individual containers for the FastAPI backend, Vite frontend, and an
MLflow tracking server.

## Services
| Service | Image | Ports | Notes |
|---------|-------|-------|-------|
| `backend` | Built from `backend/Dockerfile` | 8000 | FastAPI API with Poetry deps; connects to MLflow via `MLFLOW_TRACKING_URI`. |
| `frontend` | Built from `frontend/Dockerfile` | 5173 | Serves the production Vite build via `serve`. Uses `VITE_API_BASE_URL` build arg to target `backend`. |
| `mlflow` | `ghcr.io/mlflow/mlflow` | 5000 | Logs experiments to `mlruns/` (mounted volume). |

## Prerequisites
- Docker and Docker Compose v2+
- `backend/.env` containing the RapidAPI credentials
- Optional: ensure `mlruns/` exists (it's ignored in Git and created automatically otherwise)

## Usage
```bash
docker compose up --build
```

Once healthy:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- MLflow UI: http://localhost:5500 (port mapped to 5000 inside the container)

The backend container automatically sends lightweight metrics for each `/match` call to MLflow.

## Environment Variables
| Variable | Location | Description |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | frontend build arg | Points the Vite bundle to the backend service (defaults to `http://backend:8000`). |
| `MLFLOW_TRACKING_URI` | backend service env | Defaults to `http://mlflow:5000`; override if you host MLflow elsewhere. |

To scale or replace services (e.g., swap MLflow for another tracker), edit `docker-compose.yml`.
