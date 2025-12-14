# backend/app.py
import json
import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Annotated, Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .job_fetcher import fetch_jobs_from_api, fetch_random_jobs
from .nlp_model.resume_parser import ResumeParser
from .nlp_model_stub import recommend_jobs

UploadedResume = Annotated[UploadFile, File(...)]

BASE_DIR = Path(__file__).resolve().parent
CACHE_PATH = BASE_DIR / "cache.json"
STATIC_DIR = BASE_DIR / "static"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs/random")
def get_random_jobs():
    """Return a random job feed for the landing page."""
    logger.info("Fetching random jobs for homepage feed.")
    results = fetch_random_jobs()
    return {"results": results}

@app.get("/jobs/search")
def search_jobs(title: str, location: str):
    """Search jobs from the external API."""
    logger.info("Searching jobs for title=%s, location=%s", title, location)
    results = fetch_jobs_from_api(title, location)
    return {"results": results}

@app.post("/match")
async def match_resume(
    file: UploadedResume,
    title: str = Form(...),
    location: Optional[str] = Form(None),
    experience: Optional[str] = Form(None),
):
    """Match a resume to jobs and return scored recommendations."""
    logger.info(
        "Received match request title=%s, location=%s, experience=%s",
        title,
        location or "",
        experience or "",
    )
    # --- Step 1: safely handle file upload ---
    suffix = os.path.splitext(file.filename)[1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # --- Step 2: extract text from resume ---
        parser = ResumeParser()
        try:
            resume_text = parser.load_resume(tmp_path)
        except Exception as err:
            logger.exception("Failed to parse resume: %s", err)
            return {"error": f"Failed to parse resume: {str(err)}", "results": []}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # --- Step 3: fetch job postings ---
    job_list = fetch_jobs_from_api(title, location or "")

    # --- Step 4: score jobs across five dimensions ---
    results = recommend_jobs(
        resume_text,
        job_list,
        title,
        location or "",
        experience or "",
    )

    # --- Step 5: cache results and return ---
    with CACHE_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f)

    logger.info("Returning %d recommendations", min(len(results), 10))
    return {"results": results[:10]}

@app.get("/match/more")
def load_more_matches():
    """Return cached recommendations from the last match request."""
    if not CACHE_PATH.exists():
        logger.warning("Cache file not found when requesting /match/more.")
        return {"results": []}
    try:
        with CACHE_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        logger.exception("Failed to load cache.json for /match/more.")
        return {"results": []}
    return {"results": data}

if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

@app.get("/")
def serve_home():
    """Serve the built frontend if available."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Frontend not built."}
