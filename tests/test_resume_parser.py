"""Tests for ResumeParser utilities."""

from backend.nlp_model.resume_parser import ResumeParser, extract_resume_skills


def test_parse_sections_and_extract_skills():
    parser = ResumeParser()
    resume_text = (
        "Jane Doe\n"
        "SUMMARY\nData analyst with ML background.\n"
        "SKILLS\nPython, SQL, AWS\n"
        "EXPERIENCE\nWorked on analytics solutions.\n"
        "EDUCATION\nBS in Computer Science\n"
    )

    sections = parser.parse_sections(resume_text)

    assert "Python" in sections["skills"]
    assert "analytics" in sections["experience"].lower()

    skills = extract_resume_skills(sections)
    assert "Python" in skills["all_skills"]
    assert skills["total_count"] >= 2
