import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymupdf
from app.services.pdf_service import extract_text_from_pdf
from app.services.skill_service import compare_skills
from app.services.ml_service import calculate_similarity_score
from app.services.chat_service import answer_resume_question

def run_tests():
    print("--- 1. Testing In-Memory PDF Creation & Extraction ---")
    doc = pymupdf.open()
    page = doc.new_page()
    sample_resume = """
    Jane Doe
    Senior Software Engineer
    Email: jane@example.com | GitHub: github.com/janedoe
    
    Technical Skills:
    Python, FastAPI, React.js, PostgreSQL, Docker, Git, REST APIs, Tailwind CSS, Problem Solving, Teamwork.
    
    Experience:
    Built high-performance microservices using FastAPI and PostgreSQL.
    Developed dynamic frontends using React.js and Tailwind CSS.
    Deployed containerized services with Docker and configured CI/CD.
    """
    page.insert_text((50, 50), sample_resume)
    pdf_bytes = doc.tobytes()
    doc.close()
    
    extracted = extract_text_from_pdf(pdf_bytes)
    assert "FastAPI" in extracted
    print(f"PDF extraction successful! Length: {len(extracted)} chars.")

    print("\n--- 2. Testing Skill Comparison ---")
    sample_jd = """
    We are looking for a Senior Python Developer with experience in:
    - Python, FastAPI, Docker, Kubernetes, AWS, PostgreSQL, GraphQL
    - Strong problem solving, collaboration, and agile mindset.
    """
    skill_results = compare_skills(extracted, sample_jd)
    print(f"Matching skills: {skill_results['matching_skills']}")
    print(f"Missing skills: {skill_results['missing_skills']}")
    assert "Python" in skill_results['matching_skills']
    assert "FastAPI" in skill_results['matching_skills']
    assert "Kubernetes" in skill_results['missing_skills']
    print("Skill comparison verified!")

    print("\n--- 3. Testing ML Similarity Scoring ---")
    sim = calculate_similarity_score(extracted, sample_jd)
    print(f"Calculated Score: {sim['match_score']}% ({sim['interpretation']})")
    assert sim['match_score'] > 0.0
    print("ML TF-IDF Cosine Similarity verified!")

    print("\n--- 4. Testing Chat Contextual Response ---")
    summary = {
        "match_score": sim['match_score'],
        "matching_skills": skill_results['matching_skills'],
        "missing_skills": skill_results['missing_skills'],
        "strengths": ["Strong backend experience in FastAPI"],
        "weaknesses": ["Missing Kubernetes orchestration"]
    }
    answer = answer_resume_question("Which skills am I missing?", summary)
    print(f"Chat answer: {answer[:120]}...")
    assert "Kubernetes" in answer
    print("Chat contextual response verified!")

    print("\nAll backend unit tests PASSED successfully!")

if __name__ == "__main__":
    run_tests()
