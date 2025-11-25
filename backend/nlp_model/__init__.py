"""
NLP Model Package for Resume Parsing and Job Matching

This package contains modules for parsing resumes, extracting skills,
and matching candidates with job opportunities.

Author: Renke Deng (Member A)
Version: 1.0
"""

from .skills_dict import (
    SKILL_DICT,
    SKILL_ALIASES,
    get_all_skills,
    normalize_skill,
    get_skills_by_category,
    get_all_categories,
    search_skills,
    get_skill_count,
    is_valid_skill
)

from .resume_parser import (
    ResumeParser,
    parse_resume,
    extract_resume_skills,
    infer_target_roles
)

__version__ = "1.0.0"
__author__ = "Renke Deng (Member A)"

__all__ = [
    # Skills dictionary
    'SKILL_DICT',
    'SKILL_ALIASES',
    'get_all_skills',
    'normalize_skill',
    'get_skills_by_category',
    'get_all_categories',
    'search_skills',
    'get_skill_count',
    'is_valid_skill',
    # Resume parser
    'ResumeParser',
    'parse_resume',
    # Division.md interface functions
    'extract_resume_skills',
    'infer_target_roles'
]
