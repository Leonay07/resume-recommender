# backend/nlp_model_stub.py

"""
NLP model for resume parsing and job matching.

This module integrates the resume parser to extract skills from resumes
and uses them for job matching.

Author: Renke Deng (Member A)
"""

import os
import tempfile
from nlp_model import ResumeParser, extract_resume_skills, infer_target_roles


def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    Recommendation function that uses the real resume parser.

    Args:
        resume_text: Raw resume text content
        job_list: List of job postings from API
        title: User-specified target job title
        location: User-specified location
        experience: User-specified years of experience

    Returns:
        List of matched jobs with scores and analysis
    """
    parser = ResumeParser()

    # Parse resume sections from text
    sections = parser.parse_sections(resume_text)

    # Extract skills using Member A's parser
    skills_result = extract_resume_skills(sections)
    extracted_skills = skills_result.get('all_skills', [])

    # Infer target roles
    target_roles = infer_target_roles(sections, title)

    # Build results for each job
    results = []
    for job in job_list:
        job_description = job.get('description', '').lower()
        job_title = job.get('title', '').lower()

        # Calculate matching score based on skill overlap
        matched_skills = []
        for skill in extracted_skills:
            if skill.lower() in job_description or skill.lower() in job_title:
                matched_skills.append(skill)

        # Calculate score (skill match ratio + role match bonus)
        skill_score = len(matched_skills) / max(len(extracted_skills), 1) if extracted_skills else 0.3

        # Role match bonus
        role_bonus = 0.0
        for role in target_roles:
            if role.lower() in job_title or role.lower() in job_description:
                role_bonus = 0.15
                break

        # Final score (capped at 1.0)
        final_score = min(skill_score * 0.8 + role_bonus + 0.1, 1.0)

        # Generate summary
        if matched_skills:
            summary = f"Your skills in {', '.join(matched_skills[:3])} match this position."
        else:
            summary = f"This {job.get('title', 'position')} may align with your career goals."

        results.append({
            "title": job.get('title', 'Unknown'),
            "company": job.get('company', 'Unknown'),
            "location": job.get('location', location or 'Remote'),
            "description": job.get('description', ''),
            "apply_link": job.get('apply_link', ''),
            "score": round(final_score, 2),
            "summary": summary,
            "keywords": matched_skills[:5] if matched_skills else extracted_skills[:5],
            "evidence_image": None,
        })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)

    return results


def parse_resume_file(file_path, user_title=None):
    """
    Parse a resume file and extract all information.

    Args:
        file_path: Path to resume file (PDF/DOCX/TXT)
        user_title: Optional user-specified job title

    Returns:
        Dictionary with parsing results
    """
    from nlp_model import parse_resume
    return parse_resume(file_path, user_title)
