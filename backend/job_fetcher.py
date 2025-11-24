# backend/job_fetcher.py

"""
Job fetching utilities with environment variable support.
Loads RAPID_API_KEY from .env using python-dotenv.
"""

import requests
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")


def fetch_jobs_from_api(title, location):
    """
    Fetch job data from the JSearch API and filter by title/location.
    Automatically fetches extra pages if fewer than 10 matched jobs.
    """
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    def get_jobs(page=1):
        params = {
            "query": f"{title} in {location}",
            "num_pages": page,
            "date_posted": "month",
            "employment_types": "FULLTIME",
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json().get("data", [])

    # First fetch
    data = get_jobs(page=1)

    job_list = []
    for j in data:
        job_title = (j.get("job_title") or "").lower()
        job_loc = (j.get("job_city") or j.get("job_state") or "").lower()

        if title.lower() in job_title and location.lower() in job_loc:
            job_list.append({
                "title": j.get("job_title"),
                "company": j.get("employer_name"),
                "location": j.get("job_city") or j.get("job_state"),
                "description": j.get("job_description"),
                "apply_link": j.get("job_apply_link"),
            })

    # If fewer than 10 jobs, fetch more
    if len(job_list) < 10:
        extra_data = get_jobs(page=2)
        for j in extra_data:
            job_title = (j.get("job_title") or "").lower()
            job_loc = (j.get("job_city") or j.get("job_state") or "").lower()

            if title.lower() in job_title and location.lower() in job_loc:
                job_list.append({
                    "title": j.get("job_title"),
                    "company": j.get("employer_name"),
                    "location": j.get("job_city") or j.get("job_state"),
                    "description": j.get("job_description"),
                    "apply_link": j.get("job_apply_link"),
                })

    return job_list


# backend/job_fetcher.py

def fetch_random_jobs():
    """
    Fetch a general list of jobs (without any title/location filter)
    and return 10 random jobs for the homepage feed.

    We call the API with a very broad query "jobs" so that it always
    returns many results, then we randomly select 10 from them.
    """

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    # Broad query to fetch many different jobs
    params = {
        "query": "jobs",
        "num_pages": 1,
        "date_posted": "month",
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", [])

    job_list = []

    # Convert API result into consistent job structure
    for j in data:
        job_list.append({
            "title": j.get("job_title"),
            "company": j.get("employer_name"),
            "location": j.get("job_city") or j.get("job_state"),
            "description": j.get("job_description"),
            "apply_link": j.get("job_apply_link"),
        })

    # Randomly sample 10 jobs (or fewer if not enough)
    return random.sample(job_list, min(10, len(job_list)))

