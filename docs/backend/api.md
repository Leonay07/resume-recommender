# Backend API Specification

The FastAPI app is defined in `backend/app.py` and exposes four public routes. The service entry point (used by Docker/HF) is:

```
uvicorn backend.app:app --host 0.0.0.0 --port 7860
```

`backend/.env` (or environment variables) must include:
```
RAPID_API_KEY=...
RAPID_API_HOST=jsearch.p.rapidapi.com
```

## Route Overview
| Path | Method | Description |
|------|--------|-------------|
| `/jobs/random` | GET | Homepage feed sourced via `fetch_random_jobs` |
| `/jobs/search` | GET | Fetch jobs filtered by title/location |
| `/match` | POST | Upload a resume and return the top 10 recommendations |
| `/match/more` | GET | Read `cache.json` for the remaining results |

### `/jobs/random`
- **Input:** none
- **Output:** `{"results": [JobItem]}` with `title`, `company`, `location`, `description`, `apply_link`.
- **Logic:** fetch “Data Scientist” jobs via RapidAPI and return a random sample of up to 10 entries.

### `/jobs/search`
- **Query params:** `title`, `location` (may be empty strings).
- **Flow:** construct `f"{title} in {location}"`, fetch up to `MAX_PAGES=3`, deduplicate `(title, company)`, and return the first `MIN_RESULTS` matches.

### `/match`
- **Fields (multipart):** `file` (UploadFile), `title`, `location` (optional), `experience` (optional).
- **Flow:**
  1. Store the file in a temp path and parse it via `ResumeParser`.
  2. Fetch jobs for the given title/location.
  3. Run `recommend_jobs` to score jobs and produce summaries.
  4. Cache the full list to `cache.json` and return the top 10.

### `/match/more`
- **Input:** none.
- **Output:** entire cache from the last `/match` call; empty list if cache is missing or unreadable.

## Data Contract
```json
{
  "title": "Data Scientist",
  "company": "Acme Corp",
  "location": "Washington, DC",
  "description": "...",
  "apply_link": "https://...",
  "score": 0.82,
  "summary": "Skills Match (80%): Python, SQL...",
  "keywords": ["python", "sql"],
  "skills": {
    "primary_skills": ["python", "sql"],
    "all_skills": ["python", "sql", "aws"],
    "skill_frequency": {"python": 3}
  }
}
```

## Implementation Notes
- `job_fetcher.py` handles pagination, deduplication, and random sampling (for `/jobs/random`). RapidAPI credentials are loaded via `python-dotenv`.
- `cache.json` lives in `backend/` (the same directory as `app.py`). The API uses `pathlib` to ensure the file is resolved correctly whether running locally or inside Docker.
- CORS is configured to allow all origins since Hugging Face serves the frontend and backend from different domains during development.

## Testing Tips
1. Mock RapidAPI responses to verify deduplication and job field normalization.
2. Use synthetic resumes to ensure `recommend_jobs` returns skills, summaries, and keywords.
3. Exercise `/match/more` after multiple `/match` calls to confirm caching works.
4. In Docker, run `curl -F "file=@resume.pdf" -F "title=..." http://localhost:7860/match` to validate multipart uploads end-to-end.
