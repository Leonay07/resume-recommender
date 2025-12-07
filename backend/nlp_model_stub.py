# backend/nlp_model_stub.py

"""
NLP model for resume parsing and job matching.

This module integrates the resume parser to extract skills from resumes
and uses them for job matching.

Author: Renke Deng (Member A)
"""

import os
import tempfile
from .nlp_model.resume_parser import (
    ResumeParser,
    extract_resume_skills,
    infer_target_roles
)

from .nlp_model.tfidf_matcher import compute_tfidf_scores
from .nlp_model.extract_job_skills_from_list import extract_job_skills_from_list


def recommend_jobs(resume_text, job_list, title, location, experience):
    parser = ResumeParser()
    sections = parser.parse_sections(resume_text)

    # 1) Skills based on resume
    skills_result = extract_resume_skills(sections)
    extracted_skills = skills_result.get('all_skills', [])

    # 2) Inferring target job positions based on the job title.
    target_roles = infer_target_roles(sections, title)

    # 3) Extracting job skills based on job descriptions
    jobs_with_skills = extract_job_skills_from_list(job_list)

    # 4) ML text matching score based on TF-IDF
    ml_scores = compute_tfidf_scores(resume_text, job_list)

    results = []
    for idx, job in enumerate(jobs_with_skills):
        job_raw = job_list[idx]
        job_desc = job_raw.get("description", "").lower()
        job_title = job_raw.get("title", "").lower()

        # Rule matching: overlapping skills
        matched_skills = []
        for skill in extracted_skills:
            if skill.lower() in job_desc or skill.lower() in job_title:
                matched_skills.append(skill)

        # Simple skill-based scoring
        skill_score = (
            len(matched_skills) / max(len(extracted_skills), 1)
            if extracted_skills else 0.3
        )

        # role bonus
        role_bonus = 0.0
        for role in target_roles:
            if role.lower() in job_title or role.lower() in job_desc:
                role_bonus = 0.15
                break

        # ML Score
        tfidf_score = ml_scores[idx]  # already in [0, 1]

        # Integration: 0.5 (skill rules) + 0.5 (ML)
        combined_score = 0.5 * (skill_score * 0.8 + role_bonus + 0.1) + 0.5 * tfidf_score
        final_score = float(min(1.0, combined_score))

        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"] or (location or "Remote"),
            "description": job["description"],
            "apply_link": job["apply_link"],
            "score": round(final_score, 2),
            "summary": (
                f"ML text similarity score = {tfidf_score:.2f}. "
                f"Matched skills: {', '.join(matched_skills[:5])}"
                if matched_skills else
                f"ML text similarity score = {tfidf_score:.2f}."
            ),
            "skills": job["skills"],  # Extracted job skills
            "keywords": matched_skills[:5] or job["skills"]["primary_skills"][:5],
            "evidence_image": None,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results