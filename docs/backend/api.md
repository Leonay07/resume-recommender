# Backend API Specification

Summarized from `03_backend_api_skeleton_v4.md`.

## Service Entry Point
- `uvicorn app:app --host 0.0.0.0 --port 7860`
- `backend/.env` must define `RAPID_API_KEY` and `RAPID_API_HOST`

## Route Overview
| Path | Method | Description |
|------|--------|-------------|
| `/jobs/random` | GET | Homepage feed sourced via `fetch_random_jobs` |
| `/jobs/search` | GET | Fetch jobs filtered by title/location |
| `/match` | POST | Upload a resume and return the top 10 recommendations |
| `/match/more` | GET | Read `cache.json` for the remaining results |

### `/jobs/random`
- Input: none
- Output: `{"results": [JobItem]}` where each item contains `title/company/location/description/apply_link`
- Logic: pick a predefined job title/location pair, call RapidAPI, and sample 10 entries.

### `/jobs/search`
Query params:
- `title` (str)
- `location` (str)

Flow:
1. Build `query = f"{title} in {location}"`.
2. Iterate up to `MAX_PAGES`, deduplicating on `(title, company)`.
3. Continue paging until at least `MIN_RESULTS` remain.

### `/match`
Multipart form fields: `file` (UploadFile), `title`, `location`, `experience`.

Steps:
1. Save the upload to a temp file and parse it with `ResumeParser`.
2. Call `fetch_jobs_from_api` to retrieve job listings.
3. Invoke `recommend_jobs` (nlp_model_stub) to compute the five scores.
4. Persist full results to `cache.json` and return `results[:10]`.

### `/match/more`
- Input: none (current version returns the entire cache; `offset/limit` can be added later).
- Output: the cached list from the last `/match` call, or an empty list when cache is missing.

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

## job_fetcher Logic
- `MIN_RESULTS=10`, `MAX_PAGES=3`.
- Reads RapidAPI credentials from `.env`.
- Deduplicates using `seen_keys` to avoid repeated `(title, company)` pairs.
- `fetch_random_jobs` defaults to “Data Scientist” and samples 10 entries.

## Caching Strategy
- File path: `backend/cache.json`
- Write: overwrite in `/match` after computing scores.
- Read: `/match/more`
- Failure guard: return `{"results": []}` when parsing fails or file is missing.

## Testing Tips
1. Mock RapidAPI responses to verify deduplication.
2. Use sample resumes to check the shape of `recommend_jobs` outputs.
3. Hit `/match/more` multiple times to confirm cache reuse.
4. Run `curl` inside Docker to validate CORS and multipart handling.
