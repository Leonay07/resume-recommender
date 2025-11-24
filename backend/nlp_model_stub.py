# backend/nlp_model_stub.py

"""
This file defines the interface for the NLP model that will be used
to rank job postings based on the user's resume and search criteria.

Team members working on the model can directly replace the logic inside
`recommend_jobs()` without changing the backend API structure.
"""

import random

def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    Recommend jobs based on resume content and user preferences.
    
    Parameters:
        resume_text (str): Extracted text from the uploaded resume.
        job_list (list): List of job dicts fetched from the job API.
        title (str): User's target job title.
        location (str): User's selected location.
        experience (str): User's experience level.

    Returns:
        list: A ranked list of job dicts, each containing:
              - title
              - company
              - location
              - description
              - apply_link
              - score (float)
    """

    # Placeholder behavior:
    # Assign a random score to each job.
    results = []
    for job in job_list:
        job_copy = job.copy()
        job_copy["score"] = round(random.uniform(70, 99), 2)
        results.append(job_copy)

    # Sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)

    return results
