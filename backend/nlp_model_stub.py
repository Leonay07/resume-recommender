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

import logging
import os
import re
import time

import requests

from .nlp_model.extract_job_skills_from_list import extract_job_skills_from_list
from .nlp_model.resume_parser import ResumeParser, extract_resume_skills, infer_target_roles
from .nlp_model.tfidf_matcher import compute_tfidf_scores

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "resume_recommender")

# Mapping of U.S. state names to abbreviations (used for location matching)
STATE_MAP = {
    "alabama": "al",
    "alaska": "ak",
    "arizona": "az",
    "arkansas": "ar",
    "california": "ca",
    "colorado": "co",
    "connecticut": "ct",
    "delaware": "de",
    "florida": "fl",
    "georgia": "ga",
    "hawaii": "hi",
    "idaho": "id",
    "illinois": "il",
    "indiana": "in",
    "iowa": "ia",
    "kansas": "ks",
    "kentucky": "ky",
    "louisiana": "la",
    "maine": "me",
    "maryland": "md",
    "massachusetts": "ma",
    "michigan": "mi",
    "minnesota": "mn",
    "mississippi": "ms",
    "missouri": "mo",
    "montana": "mt",
    "nebraska": "ne",
    "nevada": "nv",
    "new hampshire": "nh",
    "new jersey": "nj",
    "new mexico": "nm",
    "new york": "ny",
    "north carolina": "nc",
    "north dakota": "nd",
    "ohio": "oh",
    "oklahoma": "ok",
    "oregon": "or",
    "pennsylvania": "pa",
    "rhode island": "ri",
    "south carolina": "sc",
    "south dakota": "sd",
    "tennessee": "tn",
    "texas": "tx",
    "utah": "ut",
    "vermont": "vt",
    "virginia": "va",
    "washington": "wa",
    "west virginia": "wv",
    "wisconsin": "wi",
    "wyoming": "wy",
}

def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    Main recommendation function implementing the 5-Dimensional Scoring System.
    """
    
    # Return early if no jobs were fetched
    if not job_list:
        return []

    # ==========================================
    # Phase 1: user profiling
    # ==========================================
    logger.info("Starting user profile parsing...")
    parser = ResumeParser()
    sections = parser.parse_sections(resume_text)

    # Extract skills from resume sections
    skills_result = extract_resume_skills(sections)
    extracted_skills = skills_result.get('all_skills', [])
    # Normalize to lowercase set
    user_skills_set = {s.lower().strip() for s in extracted_skills}

    # Infer user intent / target roles
    target_roles = infer_target_roles(sections, title)

    # Parse years of experience
    user_yoe_is_any = False
    user_yoe = 0
    
    # Handle "No preference" inputs
    if experience and "no preference" in str(experience).lower():
        user_yoe_is_any = True
        user_yoe = 0
    else:
        try:
            user_yoe = int(re.search(r'\d+', str(experience)).group())
        except (AttributeError, ValueError):
            user_yoe = 0
    
    logger.info(
        "User parsed: %d skills, roles=%s, YoE=%d (any=%s)",
        len(user_skills_set),
        target_roles,
        user_yoe,
        user_yoe_is_any,
    )

    # ==========================================
    # Phase 2: process job data
    # ==========================================
    
    structured_jobs = extract_job_skills_from_list(job_list)
    ml_scores = compute_tfidf_scores(resume_text, job_list)

    results = []

    # ==========================================
    # Phase 3: scoring loop
    # ==========================================
    
    logger.debug("=" * 80)
    logger.debug(
        "%-20s | Skill | Seman | Role | Exp  | Loc  | ==> Final",
        "Job Title",
    )
    logger.debug("=" * 80)

    for job, tfidf_score in zip(structured_jobs, ml_scores, strict=False):
        
        job_title = job.get("title", "").lower()
        job_desc = job.get("description", "").lower()
        job_loc = job.get("location", "").lower()

        # --------------------------------------
        # Dimension 1: skill overlap (40%)
        # --------------------------------------
        raw_job_skills = job.get("skills", {}).get("all_skills", [])
        job_skills_set = {s.lower().strip() for s in raw_job_skills}
        
        matched_skills_set = user_skills_set.intersection(job_skills_set)
        matched_skills = list(matched_skills_set)
        
        # Cap denominator at 7 to avoid penalizing long job descriptions.
        denom = min(len(job_skills_set), 7)
        denom = max(denom, 1)
        
        skill_score = min(1.0, len(matched_skills) / denom)

        # --------------------------------------
        # Dimension 2: semantic (TF-IDF, 25%) multiplied by 3
        # --------------------------------------
        content_score = min(1.0, tfidf_score * 3.0)

        # --------------------------------------
        # Dimension 3: role intent match (15%)
        # --------------------------------------
        role_score = 0.0
        for role in target_roles:
            if role.lower() in job_title or role.lower() in job_desc:
                role_score = 1.0
                break
        
        # --------------------------------------
        # Dimension 4: experience alignment (10%)
        # --------------------------------------
        exp_match = re.search(r'(\d+)\+?\s*years?', job_desc)
        req_yoe = int(exp_match.group(1)) if exp_match else 0
        
        if user_yoe_is_any:
            exp_score = 1.0
        elif user_yoe >= req_yoe:
            exp_score = 1.0
        elif user_yoe >= req_yoe - 1:
            exp_score = 0.5
        else:
            exp_score = 0.0

        # --------------------------------------
        # Dimension 5: location match (10%)
        # Supports full names and state abbreviations (e.g., California -> CA)
        # --------------------------------------
        user_loc_raw = location.lower().strip() if location else ""
        user_loc_abbr = STATE_MAP.get(user_loc_raw, user_loc_raw)  # e.g., "california" -> "ca"
        
        loc_score = 0.0
        
        if "remote" in job_loc:
            loc_score = 1.0
        elif user_loc_raw and user_loc_raw in job_loc:
            loc_score = 1.0
        elif user_loc_abbr and user_loc_abbr != user_loc_raw:
            patterns = [
                f", {user_loc_abbr}",
                f",{user_loc_abbr}",
                f" {user_loc_abbr} ",
            ]
            if any(pattern in job_loc for pattern in patterns):
                loc_score = 1.0

        # ==========================================
        # Weighted combination (emphasize hard skills)
        # ==========================================
        combined_score = (skill_score * 0.40) + \
                         (content_score * 0.25) + \
                         (role_score * 0.15) + \
                         (exp_score * 0.10) + \
                         (loc_score * 0.10)
        
        final_score = float(min(1.0, combined_score))
        
        # Debug logging
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

        # Generate summary text
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
    log_recommendation_run(job_list, results, target_roles, title, location)
    return results


def log_recommendation_run(job_list, results, target_roles, title, location):
    """Record lightweight experiment metrics in MLflow via REST, if configured."""
    if not MLFLOW_TRACKING_URI:
        return
    try:
        experiment_id = _ensure_experiment(MLFLOW_EXPERIMENT_NAME)
        if not experiment_id:
            return
        run_id = _create_run(experiment_id)
        if not run_id:
            return
        params = {
            "query_title": title or "",
            "query_location": location or "",
            "target_roles": ",".join(target_roles) if target_roles else "",
        }
        metrics = {
            "jobs_fetched": len(job_list),
            "jobs_returned": len(results),
        }
        if results:
            avg_score = sum(job["score"] for job in results) / len(results)
            metrics["avg_recommendation_score"] = avg_score

        for key, value in params.items():
            _mlflow_post(
                "runs/log-parameter",
                {"run_id": run_id, "key": key, "value": value},
            )
        timestamp = int(time.time() * 1000)
        for key, value in metrics.items():
            _mlflow_post(
                "runs/log-metric",
                {"run_id": run_id, "key": key, "value": value, "timestamp": timestamp},
            )
        _mlflow_post("runs/update", {"run_id": run_id, "status": "FINISHED"})
    except requests.RequestException as exc:
        logger.debug("Skipping MLflow logging: %s", exc)
def _ensure_experiment(name: str) -> str | None:
    """Return an experiment_id, creating the experiment if required."""
    try:
        response = requests.get(
            f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/experiments/get-by-name",
            params={"experiment_name": name},
            timeout=5,
        )
        if response.status_code == 200:
            return response.json()["experiment"]["experiment_id"]
    except requests.RequestException:
        return None

    create_resp = _mlflow_post("experiments/create", {"name": name})
    if create_resp:
        return create_resp.get("experiment_id")
    return None


def _create_run(experiment_id: str) -> str | None:
    payload = {
        "experiment_id": experiment_id,
        "start_time": int(time.time() * 1000),
        "tags": [{"key": "source", "value": "resume_recommender"}],
    }
    response = _mlflow_post("runs/create", payload)
    if response:
        return response["run"]["info"]["run_id"]
    return None


def _mlflow_post(path: str, payload: dict) -> dict | None:
    url = f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/{path}"
    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()
