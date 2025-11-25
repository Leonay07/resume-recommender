# 模块 03：后端接口骨架（v4 最终版）

## 🎯 模块目标
构建完整 FastAPI 后端，实现岗位抓取、智能初筛、随机展示、NLP 模型调用与分页缓存逻辑，支持从首页展示到个性化推荐的完整流程（适配 Hugging Face Spaces 部署）。

---

## 一、功能概述
| 编号 | 功能模块 | 说明 |
|------|-----------|------|
| 1️⃣ | 首页岗位展示 `/jobs/random` | 抓取随机岗位用于首页Feed初始展示 |
| 2️⃣ | 精准岗位抓取 `/jobs/search` | 根据title/location抓取匹配岗位 |
| 3️⃣ | NLP 模型集成 `/match` | 上传简历 + 抓取岗位 + 模型计算匹配度 |
| 4️⃣ | 缓存与分页 `/match/more` | 保存模型结果并分页返回 |
| 5️⃣ | 自动补抓机制 | 若岗位不足10条则自动爬取下一页 |

---

## 二、后端结构
```
backend/
│
├── app.py                # 主后端接口逻辑
├── job_fetcher.py        # 岗位抓取与初筛
├── nlp_model.py          # NLP 模型接口（由 NLP 团队实现）
└── cache.json            # 模型结果缓存文件
```

---

## 三、核心接口定义

| 接口路径 | 方法 | 功能 | 状态 |
|-----------|------|------|------|
| `/jobs/random` | GET | 首页随机展示10条岗位 | ✅ |
| `/jobs/search` | GET | 抓取岗位数据并执行初筛 | ✅ |
| `/match` | POST | 上传简历，调用 NLP 模型，缓存结果 | ✅ |
| `/match/more` | GET | 从缓存分页返回更多推荐结果 | ✅ |

---

## 四、岗位抓取逻辑（job_fetcher.py）

```python
import requests
import random

def fetch_jobs_from_api(title, location):
    """
    调用 JSearch API 抓取岗位，并根据 title/location 进行初筛。
    若岗位不足10条，将自动补抓下一页。
    """
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": "YOUR_KEY",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    def get_jobs(page=1):
        params = {
            "query": f"{title} in {location}",
            "num_pages": page,
            "date_posted": "month",
            "employment_types": "FULLTIME"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json().get("data", [])

    # Step 1: 初次抓取
    data = get_jobs(page=1)

    # Step 2: 二次过滤
    job_list = []
    for j in data:
        job_title = (j.get("job_title") or "").lower()
        job_loc = (j.get("job_city") or j.get("job_state") or "").lower()
        if title.lower() in job_title and location.lower() in job_loc:
            job_list.append({
                "title": j.get("job_title"),
                "company": j.get("employer_name"),
                "location": j.get("job_city") or j.get("job_state"),
                "description": j.get("job_description"),
                "apply_link": j.get("job_apply_link"),
            })

    # Step 3: 若不足10条自动补抓
    if len(job_list) < 10:
        extra_data = get_jobs(page=2)
        for j in extra_data:
            job_title = (j.get("job_title") or "").lower()
            job_loc = (j.get("job_city") or j.get("job_state") or "").lower()
            if title.lower() in job_title and location.lower() in job_loc:
                job_list.append({
                    "title": j.get("job_title"),
                    "company": j.get("employer_name"),
                    "location": j.get("job_city") or j.get("job_state"),
                    "description": j.get("job_description"),
                    "apply_link": j.get("job_apply_link"),
                })

    return job_list


def fetch_random_jobs():
    """
    用于首页随机展示。随机选择title/location组合调用API。
    """
    sample_titles = ["Data Scientist", "Software Engineer", "ML Engineer", "Data Analyst"]
    sample_locations = ["DC", "NY", "CA", "TX"]
    title = random.choice(sample_titles)
    location = random.choice(sample_locations)
    jobs = fetch_jobs_from_api(title, location)
    return random.sample(jobs, min(10, len(jobs)))
```

---

## 五、主接口逻辑（app.py）

```python
import os, json
from fastapi import FastAPI, UploadFile
from job_fetcher import fetch_jobs_from_api, fetch_random_jobs
import nlp_model

app = FastAPI()
CACHE_PATH = "cache.json"


@app.get("/jobs/random")
def get_random_jobs():
    """
    首页展示接口：返回随机10条岗位，不依赖简历上传。
    """
    return {"results": fetch_random_jobs()}


@app.post("/match")
async def match_resume(file: UploadFile, title: str, location: str, experience: str):
    """
    Step 1. 抓取并过滤岗位
    Step 2. 调用 NLP 模型计算匹配分
    Step 3. 缓存结果至 cache.json
    Step 4. 返回前10条结果
    """
    job_list = fetch_jobs_from_api(title, location)
    resume_text = nlp_model.parse_resume(file)
    results = nlp_model.recommend_jobs(resume_text, job_list)

    with open(CACHE_PATH, "w") as f:
        json.dump(results, f)

    return {"results": results[:10]}


@app.get("/match/more")
def get_more_results(offset: int = 10, limit: int = 10):
    """
    从缓存文件分页读取模型结果。
    offset 默认10，limit 默认10。
    """
    if not os.path.exists(CACHE_PATH):
        return {"results": []}

    with open(CACHE_PATH, "r") as f:
        all_results = json.load(f)

    return {"results": all_results[offset:offset + limit]}
```

---

## 六、数据流说明

```
首页加载 → 调用 /jobs/random 获取10条岗位
↓
用户上传简历 → 调用 /match 获取个性化推荐（前10条）
↓
结果缓存 → cache.json
↓
用户点击 “Load More” → 调用 /match/more 分页加载
```

---

## 七、数据结构规范

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 岗位标题 |
| `company` | string | 公司名称 |
| `location` | string | 州简称或城市名 |
| `description` | string | 岗位描述 |
| `apply_link` | string | 应聘链接 |
| `score` | float | 模型匹配分数（由 NLP 模型生成） |

---

## 八、职责划分

| 步骤 | 动作 | 负责人 |
|------|------|--------|
| 抓取岗位数据 | 调用外部 API 并过滤 | ✅ Yuang Li |
| 首页随机展示 | 返回10条热门岗位 | ✅ Yuang Li |
| 解析简历文本 | 从 PDF 提取文本 | ⚙️ NLP 团队 |
| 匹配计算 | 语义相似度评分 | ⚙️ NLP 团队 |
| 分页与缓存 | 输出分页结果 | ✅ Yuang Li |

---

## 九、测试要点

| 测试项 | 目标 | 验证方式 |
|--------|------|----------|
| `/jobs/random` | 首页可获取岗位数据 | 加载后返回10条岗位 |
| Job API 抓取 | 成功返回100条岗位 | 打印字段完整性 |
| 过滤逻辑 | 确保title/location匹配 | 断言过滤结果正确 |
| 模型连通性 | mock NLP 模型返回分数 | 验证score字段存在 |
| 缓存 | 结果成功写入 cache.json | 查看文件内容 |
| `/match/more` | 分页正常 | offset=10时返回第11-20条 |

---

## 十、完成标准
- ✅ `/jobs/random` 首页接口可返回岗位卡片；  
- ✅ `/match` 能生成推荐结果（Top10）；  
- ✅ `/match/more` 可正常分页；  
- ✅ 自动补抓机制有效；  
- ✅ 缓存逻辑正常；  
- ✅ 全流程前后端调用一致；  
- ✅ 适配 Hugging Face 无数据库运行环境。

---

## 十一、扩展建议
- ⚙️ 引入 SQLite / Redis 持久缓存；  
- ⚙️ 增加岗位关键词相似匹配（title embedding）；  
- ⚙️ 支持动态岗位抓取（load more 自动补页）；  
- ⚙️ 增加 API 请求限流保护。
