# backend/nlp_model_stub.py
import re
from nlp_model.resume_parser import ResumeParser, extract_resume_skills, infer_target_roles
from nlp_model.extract_job_skills_from_list import extract_job_skills_from_list
from nlp_model.tfidf_matcher import compute_tfidf_scores

def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    五维评分逻辑实现
    """
    
    # === 1. 解析用户 ===
    parser = ResumeParser()
    sections = parser.parse_sections(resume_text)
    
    # 提取技能 & 转为集合
    skills_result = extract_resume_skills(sections)
    user_skills_set = set(skills_result.get('all_skills', []))
    
    # 推断意图
    target_roles = infer_target_roles(sections, title)
    
    # 解析用户经验字符串 ("3 years" -> 3)
    try:
        user_yoe = int(re.search(r'\d+', str(experience)).group())
    except:
        user_yoe = 0

    # === 2. 解析职位 ===
    # 结构化处理：调用清洗技能
    structured_jobs = extract_job_skills_from_list(job_list)
    
    # 语义处理：计算 TF-IDF 相似度
    ml_scores = compute_tfidf_scores(resume_text, job_list)

    results = []

    # === 3. 循环打分 ===
    for job, tfidf_score in zip(structured_jobs, ml_scores):
        
        # 准备数据
        job_title = job.get("title", "").lower()
        job_desc = job.get("description", "").lower()
        job_loc = job.get("location", "").lower()
        
        # --- [维度1] 技能匹配 (35%) ---
        # 使用队友清洗过的标准化技能集合
        job_skills_set = set(job.get("skills", {}).get("all_skills", []))
        matched_skills = list(user_skills_set.intersection(job_skills_set))
        # 避免分母为0
        skill_score = len(matched_skills) / max(len(job_skills_set), 1)

        # --- [维度2] 语义匹配 (30%) ---
        content_score = tfidf_score

        # --- [维度3] 角色意图 (15%) ---
        role_score = 0.0
        for role in target_roles:
            if role.lower() in job_title or role.lower() in job_desc:
                role_score = 1.0
                break
        
        # --- [维度4] 经验匹配 (10%) ---
        # 正则提取 JD 里的 "5+ years"
        exp_match = re.search(r'(\d+)\+?\s*years?', job_desc)
        req_yoe = int(exp_match.group(1)) if exp_match else 0
        
        if user_yoe >= req_yoe:
            exp_score = 1.0
        elif user_yoe >= req_yoe - 1:
            exp_score = 0.5
        else:
            exp_score = 0.0

        # --- [维度5] 地点匹配 (10%) ---
        user_loc_str = location.lower().strip() if location else ""
        if "remote" in job_loc:
            loc_score = 1.0
        elif user_loc_str and user_loc_str in job_loc:
            loc_score = 1.0
        else:
            loc_score = 0.0

        # === 最终公式 ===
        combined_score = (skill_score * 0.35) + \
                         (content_score * 0.30) + \
                         (role_score * 0.15) + \
                         (exp_score * 0.10) + \
                         (loc_score * 0.10)
        
        final_score = float(min(1.0, combined_score))

        # 生成摘要
        if len(matched_skills) > 0:
            summary = f"Skills Match: {', '.join(matched_skills[:3])}..."
        elif content_score > 0.4:
            summary = f"High Context Match ({int(content_score*100)}%)"
        else:
            summary = "Potential match based on role."

        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"] or "Remote",
            "description": job["description"],
            "apply_link": job["apply_link"],
            "score": round(final_score, 2),
            "summary": summary,
            "skills": job["skills"],
            "keywords": matched_skills[:5],
            "evidence_image": None
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results