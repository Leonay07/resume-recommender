# backend/app.py
"""
Main FastAPI application (Module 03 - Step 3)
Implements:
- /jobs/random
- /jobs/search
- /match (mock NLP)
- /match/more (pagination using cache.json)
"""

import os
import json
from fastapi import FastAPI, UploadFile, Form
from job_fetcher import fetch_jobs_from_api, fetch_random_jobs
from nlp_model_stub import recommend_jobs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend (Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_PATH = "cache.json"


# ------------------------------------------------------
# Random jobs for homepage
# ------------------------------------------------------
@app.get("/jobs/random")
def get_random_jobs():
    results = fetch_random_jobs()
    return {"results": results}


# ------------------------------------------------------
# Normal search by title + location
# ------------------------------------------------------
@app.get("/jobs/search")
def search_jobs(title: str, location: str):
    results = fetch_jobs_from_api(title, location)
    return {"results": results}


# ------------------------------------------------------
# Main matching endpoint (Accept PDF resume)
# ------------------------------------------------------
@app.post("/match")
async def match_resume(
    file: UploadFile = Form(...),
    title: str = Form(...),
    location: str = Form(...),
    experience: str = Form(...)
):
    """
    1. Receive resume PDF/TXT/DOCX
    2. Fetch jobs from API
    3. Stub model computes match scores
    4. Save full results in cache.json
    5. Return top 10
    """

    # Step 1: fetch job list
    job_list = fetch_jobs_from_api(title, location)

    # Step 2: read resume bytes (not parsing PDF here)
    resume_bytes = await file.read()
    resume_text = resume_bytes.decode("utf-8", errors="ignore")  # Stub only

    # Step 3: call stub matching model
    results = recommend_jobs(resume_text, job_list, title, location, experience)

    # Step 4: save entire result list
    with open(CACHE_PATH, "w") as f:
        json.dump(results, f)

    # Step 5: return top 10
    return {"results": results[:10]}


# ------------------------------------------------------
# Load more matched jobs
# ------------------------------------------------------
@app.get("/match/more")
def load_more_matches():
    if not os.path.exists(CACHE_PATH):
        return {"results": []}

    try:
        with open(CACHE_PATH, "r") as f:
            data = json.load(f)
    except:
        return {"results": []}

    if not isinstance(data, list):
        return {"results": []}

    return {"results": data}


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve built frontend files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")
