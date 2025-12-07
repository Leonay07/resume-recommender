# backend/nlp_model_stub.py

"""
NLP Model Integration Layer

This module orchestrates the matching process by combining:
1. Structured Skill Matching (using extract_job_skills_from_list)
2. Semantic Matching (using tfidf_matcher)
3. Role Intent Inference (using resume_parser)
4. Heuristic Rules (Experience & Location)

Author: Integration Lead
"""

import re
import logging
# 使用绝对引用，确保在 app.py 启动时不报错
from nlp_model.resume_parser import ResumeParser, extract_resume_skills, infer_target_roles
from nlp_model.extract_job_skills_from_list import extract_job_skills_from_list
from nlp_model.tfidf_matcher import compute_tfidf_scores

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    Main recommendation function implementing the 5-Dimensional Scoring System.
    """
    
    # ==========================================
    # Phase 1: 解析用户数据 (User Profiling)
    # ==========================================
    logger.info("Starting user profile parsing...")
    parser = ResumeParser()
    sections = parser.parse_sections(resume_text)

    # A. 提取用户技能 (User Skills)
    skills_result = extract_resume_skills(sections)
    extracted_skills = skills_result.get('all_skills', [])
    # 关键修正：转为小写集合，确保匹配时不区分大小写
    user_skills_set = {s.lower().strip() for s in extracted_skills}

    # B. 推断目标角色 (User Intent)
    target_roles = infer_target_roles(sections, title)

    # C. 解析用户经验 (User Experience)
    # 从字符串 "3 years" 中提取数字 3
    try:
        user_yoe = int(re.search(r'\d+', str(experience)).group())
    except:
        user_yoe = 0
    
    logger.info(f"User Parsed - Skills: {len(user_skills_set)}, Roles: {target_roles}, YoE: {user_yoe}")

    # ==========================================
    # Phase 2: 解析职位数据 (Job Processing)
    # ==========================================
    
    # D. 结构化处理 (Structured Processing)
    # 调用队友的代码，把 raw job list 变成带有 'skills' 字段的结构化列表
    structured_jobs = extract_job_skills_from_list(job_list)

    # E. 语义处理 (Semantic Processing)
    # 计算简历全文和所有 JD 的相似度
    ml_scores = compute_tfidf_scores(resume_text, job_list)

    results = []

    # ==========================================
    # Phase 3: 循环打分 (Scoring Loop)
    # ==========================================
    
    print("\n" + "="*80)
    print(f"{'Job Title':<20} | Skill | Seman | Role | Exp  | Loc  | ==> Final")
    print("="*80)

    # 使用 zip 同时遍历「结构化职位」和「ML分数」
    for job, tfidf_score in zip(structured_jobs, ml_scores):
        
        job_title = job.get("title", "").lower()
        job_desc = job.get("description", "").lower()
        job_loc = job.get("location", "").lower()

        # --------------------------------------
        # 维度 1: 技能匹配 (Skills) - 权重 35%
        # --------------------------------------
        # 获取职位要求的技能，并同样转为小写集合
        raw_job_skills = job.get("skills", {}).get("all_skills", [])
        job_skills_set = {s.lower().strip() for s in raw_job_skills}
        
        # 计算交集
        matched_skills_set = user_skills_set.intersection(job_skills_set)
        matched_skills = list(matched_skills_set) # 这里的技能名是小写的
        
        # 分母保护：防止除以0
        denom = max(len(job_skills_set), 1)
        skill_score = len(matched_skills) / denom

        # --------------------------------------
        # 维度 2: 语义匹配 (TF-IDF) - 权重 30%
        # --------------------------------------
        content_score = tfidf_score

        # --------------------------------------
        # 维度 3: 职位意图 (Role) - 权重 15%
        # --------------------------------------
        role_score = 0.0
        # 只要 Title 或 Description 包含推断出的目标角色
        for role in target_roles:
            if role.lower() in job_title or role.lower() in job_desc:
                role_score = 1.0
                break
        
        # --------------------------------------
        # 维度 4: 经验匹配 (Experience) - 权重 10%
        # --------------------------------------
        # 正则提取 JD 里的 "5+ years"
        exp_match = re.search(r'(\d+)\+?\s*years?', job_desc)
        if exp_match:
            req_yoe = int(exp_match.group(1))
        else:
            req_yoe = 0 # 没写就当 0
        
        if user_yoe >= req_yoe:
            exp_score = 1.0
        elif user_yoe >= req_yoe - 1:
            exp_score = 0.5
        else:
            exp_score = 0.0

        # --------------------------------------
        # 维度 5: 地点匹配 (Location) - 权重 10%
        # --------------------------------------
        user_loc_pref = location.lower().strip() if location else ""
        
        if "remote" in job_loc:
            loc_score = 1.0
        elif user_loc_pref and user_loc_pref in job_loc:
            loc_score = 1.0
        else:
            loc_score = 0.0

        # ==========================================
        # 4. 最终加权公式 (Total Score)
        # ==========================================
        combined_score = (skill_score * 0.35) + \
                         (content_score * 0.30) + \
                         (role_score * 0.15) + \
                         (exp_score * 0.10) + \
                         (loc_score * 0.10)
        
        final_score = float(min(1.0, combined_score))
        
        # 打印调试信息 (保留你喜欢的调试格式)
        print(f"{job['title'][:15]:<20} | {skill_score:.2f}  | {content_score:.2f}  | {role_score:.1f}  | {exp_score:.1f}  | {loc_score:.1f}  | ==> {final_score:.2f}")

        # ==========================================
        # 5. 生成智能摘要 (Smart Summary)
        # ==========================================
        if len(matched_skills) > 0:
            # 这里的 matched_skills 是小写的，为了展示好看，可以用 .title()
            display_skills = [s.title() for s in matched_skills[:3]]
            summary = f"Skills Match ({int(skill_score*100)}%): {', '.join(display_skills)}..."
        elif content_score > 0.4:
            summary = f"Strong Resume Context Match ({int(content_score*100)}%)"
        elif loc_score > 0.9:
            summary = f"Location Match: {job.get('location')}"
        else:
            summary = "Potential match based on role alignment."

        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"] or (location or "Remote"),
            "description": job["description"],
            "apply_link": job["apply_link"],
            "score": round(final_score, 2),
            "summary": summary,
            "skills": job["skills"],       
            "keywords": matched_skills[:5], # 前端高亮显示的关键词
            "evidence_image": None,
        })

    print("="*80 + "\n")

    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results