# backend/app.py
import os
import json
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from job_fetcher import fetch_jobs_from_api, fetch_random_jobs
from nlp_model_stub import recommend_jobs
# add 引入真实的 Parser 用于正确读取 PDF/DOCX
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
    file: UploadFile = Form(...),
    title: str = Form(...),
    location: str = Form(...),
    experience: str = Form(...)
):
    # --- Step 1: 安全处理文件上传 ---
    # 获取文件后缀 (如 .pdf)
    suffix = os.path.splitext(file.filename)[1]
    
    # 创建临时文件保存二进制流
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # --- Step 2: 使用 ResumeParser 提取文本 ---
        # refine之前的乱码 Bug
        parser = ResumeParser()
        try:
            resume_text = parser.load_resume(tmp_path)
        except Exception as e:
            return {"error": f"Failed to parse resume: {str(e)}", "results": []}
        
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # --- Step 3: 抓取职位 ---
    job_list = fetch_jobs_from_api(title, location)

    # --- Step 4: 调用五维打分逻辑 ---
    results = recommend_jobs(resume_text, job_list, title, location, experience)

    # --- Step 5: 缓存并返回 ---
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