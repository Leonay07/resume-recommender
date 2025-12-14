# backend/job_fetcher.py

"""
Job fetching utilities with environment variable support.
Loads RAPID_API_KEY from .env using python-dotenv.
"""

import logging
import os
import random

import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
logger = logging.getLogger(__name__)

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")
MIN_RESULTS = 10  
MAX_PAGES = 3    


def fetch_jobs_from_api(title, location):
    """
    Fetch job data from the JSearch API.
    
    IMPROVEMENT: Removed strict Python-side filtering. 
    We rely on the API's search query ("Title in Location") to do the filtering logic.
    This prevents issues like "va" not matching "Virginia".
    """
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    effective_location = (location or "").strip()
    
    # Build a query so the API handles precise matching (e.g., "Data Scientist in Virginia").
    if effective_location:
        query = f"{title} in {effective_location}"
    else:
        query = title
    
    logger.info("Fetching jobs with query '%s'", query)

    def get_jobs(page=1):
        params = {
            "query": query,
            "page": page,
            "num_pages": 1, 
            "date_posted": "month",
            "employment_types": "FULLTIME",
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            return response.json().get("data", [])
        except Exception as e:
            logger.exception("Error fetching jobs from API page %d: %s", page, e)
            return []

    job_list = []
    seen_keys = set()
    
    # Debug counters
    total_fetched = 0

    page = 1
    while page <= MAX_PAGES:
        data = get_jobs(page=page)
        if not data:
            break
        
        total_fetched += len(data)

        for j in data:
            # Extract raw fields
            job_title_raw = j.get("job_title", "Unknown Title")
            employer = j.get("employer_name", "Unknown Company")
            
            # Remove client-side filtering; rely on API query to avoid accidental drops.
            
            # Deduplicate by title/company
            key = (job_title_raw.lower(), employer.lower())
            if key in seen_keys:
                continue
            
            job_list.append({
                "title": job_title_raw,
                "company": employer,
                "location": j.get("job_city") or j.get("job_state"),
                "description": j.get("job_description"),
                "apply_link": j.get("job_apply_link"),
            })
            seen_keys.add(key)

        # Stop once enough unique jobs are collected
        if len(job_list) >= MIN_RESULTS:
            break

        page += 1

    logger.info("Fetched %d raw jobs and kept %d unique results.", total_fetched, len(job_list))

    return job_list


def fetch_random_jobs():
    """
    Fetch a general list of jobs for homepage feed.
    """
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    params = {
        "query": "Data Scientist", # more specific than generic "jobs"
        "num_pages": 1,
        "date_posted": "month",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json().get("data", [])
    except Exception as err:
        logger.exception("Failed to fetch random jobs: %s", err)
        data = []

    job_list = []
    for j in data:
        job_list.append({
            "title": j.get("job_title"),
            "company": j.get("employer_name"),
            "location": j.get("job_city") or j.get("job_state"),
            "description": j.get("job_description"),
            "apply_link": j.get("job_apply_link"),
        })
    
    # Guard against empty results
    sample_size = min(10, len(job_list))
    if sample_size == 0:
        logger.warning("No jobs returned for random feed request.")
        return []
        
    return random.sample(job_list, sample_size)
