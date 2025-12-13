# backend/app.py
import json
import logging
import os
import shutil
import tempfile
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .job_fetcher import fetch_jobs_from_api, fetch_random_jobs
from .nlp_model.resume_parser import ResumeParser
from .nlp_model_stub import recommend_jobs

UploadedResume = Annotated[UploadFile, File(...)]

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

CACHE_PATH = "cache.json"

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
    location: str = Form(""),
    experience: str = Form(""),
):
    """Match a resume to jobs and return scored recommendations."""
    logger.info(
        "Received match request title=%s, location=%s, experience=%s",
        title,
        location,
        experience,
    )
    # --- Step 1: 安全处理文件上传 ---
    suffix = os.path.splitext(file.filename)[1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # --- Step 2: 提取文本 ---
        parser = ResumeParser()
        try:
            resume_text = parser.load_resume(tmp_path)
        except Exception as err:
            logger.exception("Failed to parse resume: %s", err)
            return {"error": f"Failed to parse resume: {str(err)}", "results": []}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # --- Step 3: 抓取职位 ---
    job_list = fetch_jobs_from_api(title, location)

    # --- Step 4: 五维打分 ---
    results = recommend_jobs(resume_text, job_list, title, location, experience)

    # --- Step 5: 保存并返回 ---
    with open(CACHE_PATH, "w") as f:
        json.dump(results, f)

    logger.info("Returning %d recommendations", min(len(results), 10))
    return {"results": results[:10]}

@app.get("/match/more")
def load_more_matches():
    """Return cached recommendations from the last match request."""
    if not os.path.exists(CACHE_PATH):
        logger.warning("Cache file not found when requesting /match/more.")
        return {"results": []}
    try:
        with open(CACHE_PATH, "r") as f:
            data = json.load(f)
    except Exception:
        logger.exception("Failed to load cache.json for /match/more.")
        return {"results": []}
    return {"results": data}

if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def serve_home():
    """Serve the built frontend if available."""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Frontend not built."}
