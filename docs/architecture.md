# Architecture & Execution Order

## System Diagram
```
[Frontend (Vite/React)] --HTTP--> [FastAPI Backend]
      ↑                                  ↓
  (Resume upload)           [ResumeParser / NLP Scorer]
                                    ↓
                           [JSearch API via job_fetcher]
                                    ↓
                              [cache.json pagination]
```
- **Frontend**: Landing/Search/Result/JobDetail pages call `/jobs/random`, `/jobs/search`, `/match`, `/match/more` via `fetch`.
- **Backend**: `app.py` manages routing, file storage, caching, and static assets; `job_fetcher` wraps RapidAPI requests/deduping; `nlp_model` houses the skill dictionary, parser, and recommender.
- **Data layer**: No persistent database—RapidAPI provides live data while `cache.json` stores temporary results. API keys are injected via `.env` during deployment.

## Module Dependency Chain
From `00_development_sequence.md`:
1. Initialize repo and dependencies to stabilize the folder structure.
2. Design frontend layout/navigation (`02_frontend_layout_structure.md`).
3. Build the FastAPI skeleton (`03_backend_api_skeleton_v4.md`).
4. Extend `job_fetcher` to bridge backend and NLP (module “07”).
5. Define the NLP interface inside `nlp_model_stub` so the NLP team can implement real logic.
6. Run frontend/backend integration tests covering upload forms, CORS, caching (`05_frontend_backend_integration_v3.md`).
7. Package everything with `06_docker_deployment_guide.md` and deploy to Hugging Face.

## Key Design Choices
- **Secure uploads**: use `tempfile.NamedTemporaryFile` and delete files after parsing to avoid disk residue.
- **Job refetching**: `job_fetcher` iterates up to `MAX_PAGES` and deduplicates on `(title, company)` to maintain variety.
- **Parsing strategy**: ResumeParser supports pdfplumber/python-docx, detects sections via multi-level keywords, and shares the skill dictionary across resumes/JDs.
- **Recommendation logic**: five weighted factors (skills 40% + TF–IDF 25% + intent 15% + experience 10% + location 10%) with human-readable summaries.
- **Caching/pagination**: persist recommendations to `cache.json` so `/match/more` can serve additional pages without recomputation.
- **Microservices**: `docker-compose.yml` orchestrates three containers—frontend, backend, and MLflow—so each concern can scale independently.
- **Experiment tracking**: the backend logs lightweight metrics (jobs fetched, average scores, intent roles) to MLflow; the Compose stack exposes the UI on port 5000.

## Dependency Table
| Order | Module | Inputs | Outputs |
|-------|--------|--------|---------|
| 1 | 01 Initialization | Environment + scaffolding | `frontend/`, `backend/` layout |
| 2 | 02 Frontend Layout | Wireframes | Landing/Search/Result page skeletons |
| 3 | 03 Backend API | FastAPI | `jobs/*`, `match` endpoints |
| 4 | 07 Backend⇄NLP | Module 03 | `job_fetcher` + model pipeline |
| 5 | 05 Model Stub | Module 07 | `recommend_jobs` contract |
| 6 | 04 FE-BE Integration | 02 + 03 + 05 | Integration artifacts, API docs |
| 7 | 06 Deployment Guide | All modules | Dockerfile, HF deployment steps |

## Test Checklist
- Job API: inspect `DEBUG` logs and ensure at least 10 results after deduping.
- Resume parsing: assert pdfplumber/python-docx extraction produces sections.
- Recommendation output: each item must include `score`, `summary`, and `keywords`.
- Cache pagination: simulate repeated `/match/more` calls to ensure cache reuse.
- Docker: run `docker build` + `docker run` locally and open `http://localhost:7860`.
