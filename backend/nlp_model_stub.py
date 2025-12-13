# backend/nlp_model_stub.py

"""
NLP Model Integration Layer

This module orchestrates the matching process by combining:
1. Structured Skill Matching (using extract_job_skills_from_list)
2. Semantic Matching (using tfidf_matcher)
3. Role Intent Inference (using resume_parser)
4. Heuristic Rules (Experience & Location) - ENHANCED & OPTIMIZED VERSION

Author: Integration Lead
"""

import re
import logging
# 使用绝对引用
from nlp_model.resume_parser import ResumeParser, extract_resume_skills, infer_target_roles
from nlp_model.extract_job_skills_from_list import extract_job_skills_from_list
from nlp_model.tfidf_matcher import compute_tfidf_scores

logger = logging.getLogger(__name__)

# [新增] 美国州名到缩写的映射字典 (用于 Location 匹配)
STATE_MAP = {
    "alabama": "al", "alaska": "ak", "arizona": "az", "arkansas": "ar", "california": "ca",
    "colorado": "co", "connecticut": "ct", "delaware": "de", "florida": "fl", "georgia": "ga",
    "hawaii": "hi", "idaho": "id", "illinois": "il", "indiana": "in", "iowa": "ia",
    "kansas": "ks", "kentucky": "ky", "louisiana": "la", "maine": "me", "maryland": "md",
    "massachusetts": "ma", "michigan": "mi", "minnesota": "mn", "mississippi": "ms", "missouri": "mo",
    "montana": "mt", "nebraska": "ne", "nevada": "nv", "new hampshire": "nh", "new jersey": "nj",
    "new mexico": "nm", "new york": "ny", "north carolina": "nc", "north dakota": "nd", "ohio": "oh",
    "oklahoma": "ok", "oregon": "or", "pennsylvania": "pa", "rhode island": "ri", "south carolina": "sc",
    "south dakota": "sd", "tennessee": "tn", "texas": "tx", "utah": "ut", "vermont": "vt",
    "virginia": "va", "washington": "wa", "west virginia": "wv", "wisconsin": "wi", "wyoming": "wy"
}

def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    Main recommendation function implementing the 5-Dimensional Scoring System.
    """
    
    # 1. [安全检查] 如果 API 没抓到职位，直接返回空
    if not job_list:
        return []

    # ==========================================
    # Phase 1: 解析用户数据 (User Profiling)
    # ==========================================
    logger.info("Starting user profile parsing...")
    parser = ResumeParser()
    sections = parser.parse_sections(resume_text)

    # A. 提取用户技能 (User Skills)
    skills_result = extract_resume_skills(sections)
    extracted_skills = skills_result.get('all_skills', [])
    # 转为小写集合
    user_skills_set = {s.lower().strip() for s in extracted_skills}

    # B. 推断目标角色 (User Intent)
    target_roles = infer_target_roles(sections, title)

    # C. 解析用户经验 (User Experience)
    user_yoe_is_any = False
    user_yoe = 0
    
    # [逻辑修复] 处理 "No preference"
    if experience and "no preference" in str(experience).lower():
        user_yoe_is_any = True
        user_yoe = 0 
    else:
        try:
            user_yoe = int(re.search(r'\d+', str(experience)).group())
        except:
            user_yoe = 0
    
    logger.info(f"User Parsed - Skills: {len(user_skills_set)}, Roles: {target_roles}, YoE: {user_yoe} (Any={user_yoe_is_any})")

    # ==========================================
    # Phase 2: 解析职位数据 (Job Processing)
    # ==========================================
    
    structured_jobs = extract_job_skills_from_list(job_list)
    ml_scores = compute_tfidf_scores(resume_text, job_list)

    results = []

    # ==========================================
    # Phase 3: 循环打分 (Scoring Loop)
    # ==========================================
    
    logger.debug("=" * 80)
    logger.debug(
        "%-20s | Skill | Seman | Role | Exp  | Loc  | ==> Final",
        "Job Title",
    )
    logger.debug("=" * 80)

    for job, tfidf_score in zip(structured_jobs, ml_scores):
        
        job_title = job.get("title", "").lower()
        job_desc = job.get("description", "").lower()
        job_loc = job.get("location", "").lower()

        # --------------------------------------
        # 维度 1: 技能匹配 (Skills) - 权重 40% (提升权重)
        # --------------------------------------
        raw_job_skills = job.get("skills", {}).get("all_skills", [])
        job_skills_set = {s.lower().strip() for s in raw_job_skills}
        
        matched_skills_set = user_skills_set.intersection(job_skills_set)
        matched_skills = list(matched_skills_set)
        
        # [分数优化] 设置分母上限。只要命中 7 个核心技能就算满分。
        # 防止 JD 堆砌 30 个技能导致分数过低。
        denom = min(len(job_skills_set), 7)
        denom = max(denom, 1) # 防止除以0
        
        skill_score = min(1.0, len(matched_skills) / denom)

        # --------------------------------------
        # 维度 2: 语义匹配 (TF-IDF) - 权重 25% (降低权重，放大数值)
        # --------------------------------------
        # [分数优化] TF-IDF 原始分通常在 0.1~0.3，我们给它乘以 3.0 的倍率
        content_score = min(1.0, tfidf_score * 3.0)

        # --------------------------------------
        # 维度 3: 职位意图 (Role) - 权重 15%
        # --------------------------------------
        role_score = 0.0
        for role in target_roles:
            if role.lower() in job_title or role.lower() in job_desc:
                role_score = 1.0
                break
        
        # --------------------------------------
        # 维度 4: 经验匹配 (Experience) - 权重 10%
        # --------------------------------------
        exp_match = re.search(r'(\d+)\+?\s*years?', job_desc)
        req_yoe = int(exp_match.group(1)) if exp_match else 0
        
        if user_yoe_is_any:
            exp_score = 1.0  # 用户无偏好 -> 满分
        elif user_yoe >= req_yoe:
            exp_score = 1.0
        elif user_yoe >= req_yoe - 1:
            exp_score = 0.5
        else:
            exp_score = 0.0

        # --------------------------------------
        # 维度 5: 地点匹配 (Location) - 权重 10%
        # --------------------------------------
        # [逻辑修复] 支持全称转缩写匹配 (California -> CA)
        user_loc_raw = location.lower().strip() if location else ""
        user_loc_abbr = STATE_MAP.get(user_loc_raw, user_loc_raw) # 比如 "california" -> "ca"
        
        loc_score = 0.0
        
        if "remote" in job_loc:
            loc_score = 1.0
        elif user_loc_raw and user_loc_raw in job_loc:
            loc_score = 1.0  # 全名匹配
        elif user_loc_abbr and user_loc_abbr != user_loc_raw:
             # 缩写匹配逻辑 (加边界检查防止误判)
             if f", {user_loc_abbr}" in job_loc or f",{user_loc_abbr}" in job_loc or f" {user_loc_abbr} " in job_loc:
                 loc_score = 1.0

        # ==========================================
        # 4. [分数优化] 最终加权公式
        # ==========================================
        # 侧重硬技能，减少玄学语义的拖累
        combined_score = (skill_score * 0.40) + \
                         (content_score * 0.25) + \
                         (role_score * 0.15) + \
                         (exp_score * 0.10) + \
                         (loc_score * 0.10)
        
        final_score = float(min(1.0, combined_score))
        
        # 打印调试信息
        logger.debug(
            "%-20s | %.2f  | %.2f  | %.1f  | %.1f  | %.1f  | ==> %.2f",
            job["title"][:15],
            skill_score,
            content_score,
            role_score,
            exp_score,
            loc_score,
            final_score,
        )

        # --- 生成摘要 ---
        if len(matched_skills) > 0:
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
            "keywords": matched_skills[:5],
            "evidence_image": None,
        })

    logger.debug("=" * 80)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
