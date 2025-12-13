# Project Overview

## Goal
Resume Recommender lets a user upload a PDF/DOCX resume, fetches relevant jobs from RapidAPI’s JSearch feed, and returns explainable recommendations. The full stack is deployed on Hugging Face Spaces via Docker, packaging the React/Vite frontend together with the FastAPI backend for an end‑to‑end demo.

## System Components
| Module | Technology | Description |
|--------|------------|-------------|
| Frontend | React + Vite + TypeScript | Handles resume upload, job search, and result presentation |
| Backend | FastAPI + python-multipart | Orchestrates job fetching, resume parsing, recommendation scoring, and caching |
| NLP | ResumeParser + TF–IDF + heuristic engine | Extracts skills/intent and calculates five scoring dimensions |
| Deployment | Docker + Hugging Face Spaces | Multi-stage build that bundles static assets and exposes port 7860 |

## Workflow
1. The user uploads a resume and enters title/location/experience preferences in the frontend.
2. FastAPI stores the file temporarily and lets ResumeParser extract plain text plus skills.
3. `job_fetcher` queries the JSearch API, deduplicates `(title, company)`, and fills the job list.
4. The NLP layer combines skill overlap, TF–IDF similarity, role intent, experience, and location scoring.
5. Results are written to `cache.json`; the frontend renders the top 10 and can request “Load More”.

## Module Dependency Order
01 Initialization → 02 Frontend Layout → 03 Backend Skeleton → 07 Job Fetching → 05 Model Interface → 04 Frontend/Backend Integration → 06 Docker Deployment. This sequence mirrors the team planning documents so every downstream stage receives usable upstream artifacts.

## Grading Focus
- **Reproducible**: scripts, Docker build, and cloud deployment must run as documented.
- **End-to-end**: real API data flows through resume parsing and the recommendation model.
- **Engineering**: modular layout, logging, and caching strategies keep the system extensible.
- **Demo-ready**: documentation, scripts, and demo flow let the TA verify functionality quickly.
