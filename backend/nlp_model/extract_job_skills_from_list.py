"""
Job Skill Extraction Module

This module provides helper functions to extract technical skills
from job descriptions using the shared skill dictionary (skills_dict.py).

- extract_job_skills_from_description: extract skills from a single JD
- extract_job_skills_from_list: process a list of jobs and attach skills info

Author: (your name, Member C)
"""



from typing import List, Dict, Any, Optional
import re

from .skills_dict import get_all_skills, normalize_skill



def extract_job_skills_from_description(
    description: str,
    all_skills: List[str]
) -> Dict[str, Any]:
    """
    Extract skills from a single job description based on predefined skill lists.

    Args:
        description (str): The job description text.
        all_skills (List[str]): Flattened skill list from SKILL_DICT.

    Returns:
        Dict[str, Any]: A dictionary containing extracted skill information:
            {
                "primary_skills": [...],
                "secondary_skills": [...],
                "all_skills": [...],
                "skill_frequency": {...},
                "total_count": int
            }
    """
    primary_skills = set()
    secondary_skills = set()  # kept empty for structure consistency
    skill_frequency: Dict[str, int] = {}

    if not description:
        return {
            "primary_skills": [],
            "secondary_skills": [],
            "all_skills": [],
            "skill_frequency": {},
            "total_count": 0
        }

    for skill in all_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        matches = re.findall(pattern, description, flags=re.IGNORECASE)

        if matches:
            normalized = normalize_skill(skill)
            primary_skills.add(normalized)
            skill_frequency[normalized] = skill_frequency.get(normalized, 0) + len(matches)

    all_skill_set = primary_skills.union(secondary_skills)

    return {
        "primary_skills": sorted(list(primary_skills)),
        "secondary_skills": sorted(list(secondary_skills)),
        "all_skills": sorted(list(all_skill_set)),
        "skill_frequency": skill_frequency,
        "total_count": len(all_skill_set)
    }


def extract_job_skills_from_list(
    job_list: List[Dict[str, Any]],
    skill_dict: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Extract required job skills from job_list using job['description'].

    Args:
        job_list (List[Dict]): List of job dictionaries fetched from backend/APIs.
        skill_dict (Optional[Dict]): Custom skill dictionary similar to SKILL_DICT.
                                     If None, default SKILL_DICT is used.

    Returns:
        List[Dict[str, Any]]: A list of job items with standardized fields and
                              extracted skill information:
            {
                "title": str,
                "company": str,
                "location": str,
                "description": str,
                "apply_link": str,
                "skills": {
                    "primary_skills": [...],
                    "secondary_skills": [...],
                    "all_skills": [...],
                    "skill_frequency": {...},
                    "total_count": int
                }
            }
    """
    # Determine which skill list to use
    if skill_dict is not None:
        merged = []
        for value in skill_dict.values():
            if isinstance(value, (list, tuple, set)):
                merged.extend(value)
            elif isinstance(value, str):
                merged.append(value)

        all_skills = sorted({
            normalize_skill(s) for s in merged if isinstance(s, str)
        })
    else:
        all_skills = get_all_skills()

    results: List[Dict[str, Any]] = []

    # Process each job in job_list
    for job in job_list:
        title = str(job.get("title", "")).strip()
        company = str(job.get("company", "")).strip()
        location = str(job.get("location", "")).strip()
        description = str(job.get("description", "")).strip()
        apply_link = str(job.get("apply_link", "")).strip()

        skills_info = extract_job_skills_from_description(
            description=description,
            all_skills=all_skills,
        )

        results.append({
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "apply_link": apply_link,
            "skills": skills_info
        })

    return results
