"""Tests for high-level recommend_jobs scoring."""

from backend.nlp_model_stub import recommend_jobs


def test_recommend_jobs_prioritizes_strong_skill_match():
    resume_text = "Experienced Python engineer working with AWS and data pipelines."
    job_list = [
        {
            "title": "Python Engineer",
            "company": "Acme",
            "location": "California",
            "description": "Looking for Python developers with AWS experience.",
            "apply_link": "https://example.com/python",
        },
        {
            "title": "Support Specialist",
            "company": "Other",
            "location": "California",
            "description": "Provide phone support and scheduling.",
            "apply_link": "https://example.com/support",
        },
    ]

    results = recommend_jobs(
        resume_text=resume_text,
        job_list=job_list,
        title="Engineer",
        location="California",
        experience="3",
    )

    assert results, "The recommender should return at least one job"
    assert results[0]["title"] == "Python Engineer"
    assert results[0]["score"] >= results[1]["score"]
    assert "keywords" in results[0]
