# backend/nlp_model.py
"""
NLP 模型接口（模块 03 - Step 2，mock 版本）
本版本用于在模型团队接入真实 NLP 之前支持 /match 接口跑通。
包含：
- parse_resume(file): 假装解析简历
- recommend_jobs(text, job_list): 为每条岗位生成 mock 匹配 score
"""

import random


def parse_resume(file):
    """
    模拟解析简历文本，未来模块会替换为真实 PDF 提取逻辑。
    """
    return "Mock resume text extracted from PDF"


def recommend_jobs(resume_text, job_list):
    """
    模拟匹配逻辑：
    - 遍历 job_list
    - 为每条 job 随机生成一个 70~99 的 score
    - 按 score 降序排序
    """
    results = []

    for job in job_list:
        score = random.uniform(70, 99)  # 生成随机匹配度（Mock）
        results.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "description": job.get("description"),
            "apply_link": job.get("apply_link"),
            "score": round(score, 2)
        })

    # 将岗位按得分排序（高→低）
    results.sort(key=lambda x: x["score"], reverse=True)

    return results
