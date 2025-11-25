# backend/nlp_model_stub.py

"""
Temporary mock implementation of the NLP model output.
Returns fixed sample results so the UI can be tested
before the actual model integration.
"""


def recommend_jobs(resume_text, job_list, title, location, experience):
    """
    Mocked recommendation response following model_requirements_v5.
    """
    mock_results = [
        {
            "title": "Machine Learning Engineer",
            "company": "Aurora Analytics",
            "location": location or "Remote",
            "description": "Design and deploy ML systems across the Aurora platform.",
            "apply_link": "https://example.com/jobs/aurora-ml",
            "score": 0.92,
            "summary": "Your Python, AWS, and model deployment experience align well with Aurora’s stack.",
            "keywords": ["Python", "AWS", "MLOps"],
            "evidence_image": None,
        },
        {
            "title": "Data Scientist",
            "company": "Northwind Labs",
            "location": "NY",
            "description": "Own data products and experimentation for commerce analytics.",
            "apply_link": "https://example.com/jobs/northwind-ds",
            "score": 0.83,
            "summary": "Hands-on SQL and experimentation background fits this product analytics role.",
            "keywords": ["SQL", "Experimentation", "Product"],
            "evidence_image": None,
        },
        {
            "title": "AI Data Specialist",
            "company": "Kensho",
            "location": "DC",
            "description": "Partner with ML teams to build evaluation datasets and tooling.",
            "apply_link": "https://example.com/jobs/kensho-ai-data",
            "score": 0.78,
            "summary": "Experience collaborating with SMEs and annotation workflows maps to Kensho’s needs.",
            "keywords": ["Data Curation", "Annotation", "Finance"],
            "evidence_image": None,
        },
    ]
    return mock_results
