# backend/app.py
import os
import json
import shutil
import tempfile
# 1. [修正] 必须引入 File 模块
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from job_fetcher import fetch_jobs_from_api, fetch_random_jobs
from nlp_model_stub import recommend_jobs
from nlp_model.resume_parser import ResumeParser 

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
    results = fetch_random_jobs()
    return {"results": results}

@app.get("/jobs/search")
def search_jobs(title: str, location: str):
    results = fetch_jobs_from_api(title, location)
    return {"results": results}

@app.post("/match")
async def match_resume(
    # 2. [修正] 这里必须用 File(...) 而不是 Form(...)
    # 这样 Swagger 才会知道要用 multipart/form-data 发送文件
    file: UploadFile = File(...),
    title: str = Form(...),
    location: str = Form(...),
    experience: str = Form(...)
):
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
        except Exception as e:
            return {"error": f"Failed to parse resume: {str(e)}", "results": []}
        
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

    return {"results": results[:10]}

@app.get("/match/more")
def load_more_matches():
    if not os.path.exists(CACHE_PATH):
        return {"results": []}
    try:
        with open(CACHE_PATH, "r") as f:
            data = json.load(f)
    except:
        return {"results": []}
    return {"results": data}

if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def serve_home():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Frontend not built."}