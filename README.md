# Resume Recommender

**Team:** Liming Ye· Yuang Li· Yiran Tao· Renke Deng· Siyu Hu
**Live Demo:** https://huggingface.co/spaces/yl1853/dsan6700_group8
**Documentation:** TODO – link to deployed MkDocs site (or mention `mkdocs serve`)

---

## Overview

Resume Recommender ingests a user’s PDF/DOCX resume, fetches fresh job listings from RapidAPI’s JSearch feed, and ranks them with a hybrid scoring model (skills overlap, TF–IDF similarity, intent, experience, location). The stack comprises:

- **Frontend:** React + Vite + TypeScript with routed pages (Landing, Search, Result, Job Detail). API endpoints are configurable via `VITE_API_BASE_URL`.
- **Backend:** FastAPI service handling file uploads, resume parsing (pdfplumber + python-docx), RapidAPI calls, hybrid recommender, caching for “Load More,” and optional MLflow experiment logging.
- **Infrastructure:** Docker Compose spins up independent frontend, backend, and MLflow services while the root `Dockerfile` packages a single container (used on Hugging Face Spaces).
- **Tooling:** MkDocs documentation, pytest suite, Ruff linting, and GitHub Actions CI (`.github/workflows/ci.yml`) that runs lint + tests on every push/PR.

### System Architecture
`TODO – insert architecture diagram path or image`

---

## Quickstart

Choose the path that fits your needs:
- **Option A** if you plan to modify code, debug, or run tests locally.
- **Option B** if you only need a containerized demo (Docker/Hugging Face).

### Option A – Local Development (Poetry + npm)

| Step | Command | Notes |
|------|---------|-------|
| Install deps | `chmod +x setup_local.sh && ./setup_local.sh` | Installs Poetry env + frontend packages. |
| Backend dev server | `poetry run uvicorn backend.app:app --reload --port 8000` | FastAPI + live reload. |
| Frontend dev server | `cd frontend && VITE_API_BASE_URL=http://localhost:8000 npm run dev` | Vite dev server hitting the backend. |

Key endpoints:
- `GET /jobs/random`
- `GET /jobs/search?title=...&location=...`
- `POST /match` (multipart form: file, title, optional location/experience)
- `GET /match/more`

### Option B – Docker / Compose (recommended for demo)

- **Single container** (used for Hugging Face):
  ```bash
  docker build -t resume-recommender .
  docker run --rm -p 7860:7860 --env-file backend/.env resume-recommender
  ```
- **Microservice stack** (frontend + backend + MLflow):
  ```bash
  docker compose up --build
  ```

---

## Docker & Microservices

### Docker Compose (frontend + backend + MLflow)

```bash
docker compose up --build
```

| Service  | URL               | Notes                                  |
|----------|-------------------|----------------------------------------|
| frontend | http://localhost:5173 | Vite build served via `serve`.           |
| backend  | http://localhost:8000 | FastAPI API + static assets.            |
| mlflow   | http://localhost:5500 | Tracks metrics when `MLFLOW_TRACKING_URI` is set. |

Compose uses the same codebase as production, with `MLFLOW_TRACKING_URI=http://mlflow:5000`.

### Hugging Face Spaces Deployment

1. Ensure `backend/.env` contains:
   ```
   RAPID_API_KEY=...
   RAPID_API_HOST=jsearch.p.rapidapi.com
   ```
2. Run `poetry run ruff check .` and `poetry run pytest`.
3. Build locally (optional): `docker build -t resume-recommender .`.
4. Push the repo to a Docker Space (port 7860). Set Secrets `RAPID_API_KEY` and `RAPID_API_HOST`.
5. The root `Dockerfile` builds frontend → backend/static, installs FastAPI deps, and runs `uvicorn backend.app:app --port 7860`.

More details: `docs/deployment/hf.md` and `docs/deployment/compose.md`.

---

## Testing & CI

- Unit tests: `poetry run pytest`
- Linting: `poetry run ruff check .`
- GitHub Actions CI (`.github/workflows/ci.yml`) runs lint + pytest on push/PR.

---

## Experiment Tracking

- `backend/nlp_model_stub.py` logs query metadata and score metrics to MLflow over the REST API whenever `MLFLOW_TRACKING_URI` is provided (enabled automatically in Compose).
- Artifacts are stored in `./mlruns/` (ignored in Git). Hugging Face deployment omits MLflow by default unless you wire an external tracking URI.

---

## Repository Map

| Path | Description |
|------|-------------|
| `backend/` | FastAPI app, resume parser, NLP modules, job fetcher. |
| `frontend/` | React/Vite client with components, pages, styles, API helper. |
| `docs/` | MkDocs site (architecture, API, deployment). |
| `tests/` | Pytest cases for resume parser and recommender logic. |
| `docker-compose.yml` | Multi-service stack (frontend/back/MLflow). |
| `Dockerfile` | Single container build (used for Hugging Face). |
| `.github/workflows/ci.yml` | CI pipeline (ruff + pytest). |
| `discussion.pdf` | Final analysis report. |

---

## Deliverables Checklist

- [x] FastAPI backend with documented endpoints + docstrings/logging.
- [x] React/Vite frontend consuming the API via configurable base URL.
- [x] Docker Compose microservices + single Dockerfile for Hugging Face.
- [x] Experiment tracking (MLflow REST logging) and documented usage.
- [x] Static documentation (MkDocs) and final discussion PDF.
- [x] Testing + linting + GitHub Actions CI.
- [ ] README items pending: team roster, architecture diagram image, docs link, live demo URL, screenshots (optional).

Fill in the TODOs above to finalize the documentation for submission.
