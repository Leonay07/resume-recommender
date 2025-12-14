# Architecture

## System Diagram
```
[Vite Frontend]  <--HTTP-->  [FastAPI Backend]
     |                            |
     | upload + form data         |  parse resume + fetch jobs
     |                            v
     |                       [ResumeParser]
     |                            |
     |                       [Hybrid Scorer] <-- [Job Fetcher -> RapidAPI JSearch]
     |                            |
     -----------> [cache.json pagination]
```
- **Frontend** renders React routes, posts multipart forms, and fetches `/jobs/random`, `/jobs/search`, `/match`, `/match/more`.
- **Backend** (`backend/app.py`) manages uploads, temporary storage, static assets, and caches recommendations. It calls `job_fetcher.py` for RapidAPI requests and `nlp_model_stub.py` for scoring.
- **ML Layer** leverages `nlp_model/resume_parser.py`, `skills_dict.py`, `extract_job_skills_from_list.py`, and `tfidf_matcher.py`.
- **Data Layer** relies on live RapidAPI responses; the only on-disk artifacts are transient temp files and `cache.json`. Configuration comes from `backend/.env` or environment variables.

## Runtime Flow
1. **Upload** – the frontend sends a multipart request to `/match` containing the resume file and form inputs.
2. **Resume Parsing** – `ResumeParser` detects sections (skills/experience/education/projects/summary), extracts skills, and infers target roles.
3. **Job Fetching** – `fetch_jobs_from_api` builds a “title in location” query, loops up to 3 pages, deduplicates `(title, company)`, and retains essential metadata.
4. **Hybrid Scoring** – `recommend_jobs` calculates: 
   - skill overlap (40% weight),
   - TF–IDF similarity (25%),
   - role intent match (15%),
   - experience alignment (10%),
   - location match or remote allowance (10%).
   It returns scores, summaries, keyword highlights, and apply links.
5. **Caching** – results persist in `cache.json` so `/match/more` can stream the remainder without recomputing.
6. **Explainability & Logging** – debug logs print per-job scores, and when `MLFLOW_TRACKING_URI` is set, metrics are pushed to MLflow.

## Key Design Choices
- **Secure uploads** – use `tempfile.NamedTemporaryFile` and delete files immediately after parsing.
- **Graceful fallbacks** – optional location/experience fields default to empty strings; parser falls back to “other” section when headers are missing.
- **JSearch filtering** – rely on RapidAPI’s filtering to avoid brittle client-side substring checks; only deduplicate and cap the number of results.
- **Explainable output** – each recommendation includes a short summary (skills match %, location match, etc.) plus the top overlapping skills (`keywords`).
- **Microservices readiness** – Compose separates front/back-end and MLflow so each service can scale or be replaced independently.
- **Deployment parity** – the root `Dockerfile` mirrors the backend container used in Compose, ensuring Hugging Face behaves the same as local builds.

## Testing & Observability
- `tests/test_resume_parser.py` validates section parsing and skill extraction.
- `tests/test_recommend_jobs.py` ensures skill-aligned jobs outrank unrelated ones and that the recommender returns complete metadata.
- Logging is centralized via `logging.basicConfig` in `backend/app.py`; `job_fetcher.py` and `nlp_model_stub.py` emit informational statements for debugging RapidAPI queries and scoring breakdowns.
- MLflow logging can be toggled by setting `MLFLOW_TRACKING_URI` (Compose does this automatically).

## Test Checklist
- Job API: inspect `DEBUG` logs and ensure at least 10 results after deduping.
- Resume parsing: assert pdfplumber/python-docx extraction produces sections.
- Recommendation output: each item must include `score`, `summary`, and `keywords`.
- Cache pagination: simulate repeated `/match/more` calls to ensure cache reuse.
- Docker: run `docker build` + `docker run` locally and open `http://localhost:7860`.
