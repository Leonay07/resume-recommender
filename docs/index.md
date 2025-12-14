# Project Overview

## Goal
This system helps job seekers discover relevant roles by comparing their resume against live job listings. Users upload a PDF/DOCX resume, specify optional search preferences, and receive explainable recommendations. The project delivers an end‑to‑end system deployed on Hugging Face Spaces and a microservice stack runnable via Docker Compose.

## System Components
| Module | Technology | Description |
|--------|------------|-------------|
| Frontend | React + Vite + TypeScript | Routes across Landing/Search/Result/Job pages, submits forms, and renders explanations. |
| Backend | FastAPI + python-multipart | Handles file uploads, RapidAPI requests, resume parsing, scoring, caching, and static assets. |
| ML | ResumeParser + TF–IDF + heuristic engine | Extracts skills/intent and scores jobs across five weighted dimensions. |


## End-to-End Workflow
1. **Upload & Preferences** – the user uploads a PDF/DOCX resume and optionally sets title, location, and experience preferences.
2. **Resume Parsing** – FastAPI writes the file to a temp path and `ResumeParser` extracts text, sections, skills, and inferred intent.
3. **Job Fetching** – `job_fetcher` calls RapidAPI’s JSearch endpoint, paginates up to three pages, deduplicates `(title, company)`, and returns descriptions with apply links.
4. **Hybrid Scoring** – `nlp_model_stub.recommend_jobs` combines skill overlap, TF–IDF similarity, role intent, experience alignment, and location match to produce weighted scores and readable summaries.
5. **Caching & Pagination** – the ranked list is cached in `backend/cache.json`; `/match` returns the top 10 while `/match/more` streams the remainder to the frontend.
6. **Visualization** – React/Vite displays job cards, highlights overlapping skills, and surfaces apply links. Requests can be re-run with different parameters without restarting the API.

## Development & Deployment Paths
- **Local development** uses Poetry + npm for rapid iteration; `setup_local.sh` installs both environments.
- **Containerized demo** uses Docker Compose (frontend + backend + MLflow) or the single Dockerfile for Hugging Face.
- **Documentation & CI**: MkDocs provides this documentation site; GitHub Actions (`ci.yml` + `docs.yml`) run lint/tests and deploy docs to `gh-pages`.
