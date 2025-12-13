# backend/nlp_model/tfidf_matcher.py

from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_tfidf_scores(resume_text: str, job_list: List[Dict]) -> List[float]:
    """
    Compute TF-IDF cosine similarity between resume_text and each job description.

    Returns:
        A list of scores in [0, 1], aligned with job_list order.
    """
    # Collect corpus: resume + all job descriptions
    descriptions = [str(job.get("description", "") or "") for job in job_list]
    corpus = [resume_text] + descriptions

    # Fit TF-IDF on both resume and jobs
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # First row is resume, rest are jobs
    resume_vec = tfidf_matrix[0:1]
    job_vecs = tfidf_matrix[1:]

    # Cosine similarity
    sims = cosine_similarity(resume_vec, job_vecs)[0]  # shape: (n_jobs,)

    # Normalize to [0, 1] (cosine is already in [0, 1] for TF-IDF, usually)
    scores = [float(max(0.0, min(1.0, s))) for s in sims]
    return scores
