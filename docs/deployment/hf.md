# Hugging Face Spaces Deployment

## Goals
- Build frontend and backend with a single multi-stage Dockerfile.
- Run the resulting image on Hugging Face Spaces (Docker runtime).
- Keep port 7860 exposed for the React application.

## Pre-deployment Checklist
- [ ] `backend/.env` contains `RAPID_API_KEY` and `RAPID_API_HOST`
- [ ] `poetry run ruff check .` and `poetry run pytest` pass locally
- [ ] `docker compose up --build` verified locally (optional but recommended)
- [ ] Hugging Face Space uses the *Docker* runtime and Secrets include `RAPID_API_KEY`
- [ ] `huggingface.yaml` exists at the repo root

## Build & Run
```bash
# Local verification
docker build -t resume-recommender .
docker run --rm -p 7860:7860 --env-file backend/.env resume-recommender
```
- `.env` must define `RAPID_API_KEY` and `RAPID_API_HOST=jsearch.p.rapidapi.com`.
- Stage one (Node) produces the frontend assets copied into `backend/static/`.
- Stage two (Python 3.10) installs runtime deps via `pip install fastapi uvicorn[...] ... scikit-learn`.

## Dockerfile Overview
| Stage | Base image | Notes |
|-------|------------|-------|
| Frontend | `node:18` | `npm install && npm run build` → `dist/` |
| Backend | `python:3.10-slim` | Installs FastAPI/runtime deps directly via `pip install`, copies backend code + built assets |
| Entrypoint | `uvicorn backend.app:app --host 0.0.0.0 --port 7860` |

## Hugging Face Config
`huggingface.yaml`
```yaml
title: Resume Job Matcher
sdk: docker
app_port: 7860
```
Steps:
1. Create a Space with the Docker runtime and upload the repository.
2. Add `RAPID_API_KEY` (and other secrets) to the Space settings.
3. Trigger the build; once the Space shows `Running`, open the URL.

## Validation Checklist
| Step | Expectation |
|------|-------------|
| Build | Logs complete without errors and the image finishes building |
| UI | Visiting the Space URL loads the React app |
| Resume upload | `/match` returns results and `cache.json` is created |
| Load More | `/match/more` returns the full cached list |
| Logs | `uvicorn` prints request logs for debugging |

## Troubleshooting
- **Missing API key**: requests fail with 401—verify Space secrets or `.env`; local `docker run` prints a warning.
- **Static 404**: ensure `npm run build` ran and the `dist/` folder was copied.
- **CORS/upload errors**: FastAPI already uses `allow_origins="*"`; double-check frontend fetch URLs.
- **Build timeout**: keep dependencies lean (`pip install --no-cache-dir` is enabled) or restart the Space.
