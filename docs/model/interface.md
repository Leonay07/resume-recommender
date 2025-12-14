# NLP Model Interface

## Core Function
```python
def recommend_jobs(
    resume_text: str,
    job_list: list[dict],
    title: str,
    location: str,
    experience: str,
):
    """Return ranked job matches based on resume text and job list."""
```
- **resume_text**: plain text extracted by pdfplumber/python-docx.
- **job_list**: deduplicated job array returned by `fetch_jobs_from_api`.
- **title/location/experience**: user preferences from the frontend form; `experience` accepts “No preference”.

## Input Format
Each `job_list` element must include at least `title`, `company`, `location`, `description`, `apply_link`. The model should reuse this list rather than calling external APIs.

## Output Format
Return an array sorted by score descending, shaped like:
```json
{
  "title": "Machine Learning Engineer",
  "company": "Meta",
  "location": "DC",
  "description": "...",
  "score": 0.87,
  "summary": "Your Python experience strongly matches...",
  "keywords": ["python", "aws"],
  "evidence_image": null,
  "apply_link": "https://..."
}
```
- `score` must be normalized to [0, 1].
- Optional fields: `summary`, `keywords`, `evidence_image` (URL or `data:image/png;base64,...`).
- Return ≤ 10 entries; use `[]` when nothing matches.

## Implementation Notes
1. **Resume parsing**: use `ResumeParser` to split sections, extract skills, and infer intent.
2. **Skill matching**: share `skills_dict`, run `extract_job_skills_from_list` on job descriptions, and intersect with user skills.
3. **Semantic matching**: leverage `tfidf_matcher.compute_tfidf_scores`, scaling scores for interpretability.
4. **Experience/location**: regex JD text for “X years” and state abbreviations with tolerance for variants.
5. **Explainability**: craft `summary` strings such as “Skills Match (xx%): ...” using the strongest signal.

## Backend Integration
- `app.py` calls `recommend_jobs` inside `/match` and handles caching; the model should not write files.
- If the model raises exceptions, FastAPI catches them and returns `{"error": "..."}`—handle edge cases (empty job list, parsing issues) internally when possible.

## Testing Baseline
- Mock `job_list` inputs to ensure the return schema is stable.
- Add unit tests for “No preference” experience, remote roles, and state abbreviations.
- Return an empty list (not an exception) when `job_list` is empty.

## Logging & Telemetry
When `MLFLOW_TRACKING_URI` is set, `recommend_jobs` automatically sends lightweight metrics (jobs fetched/returned, average score, query context) to MLflow via REST. This is optional and primarily used in the Docker Compose stack, but it can be pointed to any tracking server.
