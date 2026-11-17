import sys
import os
import io

# Setup import path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
for p in [BACKEND_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi.testclient import TestClient
import pymupdf
from app.main import app
from app.services.pdf_service import extract_text_from_pdf
from app.services.skill_service import compare_skills
from app.services.ml_service import calculate_similarity_score
from app.services.gemini_service import generate_contextual_feedback
from app.services.chat_service import answer_resume_question

client = TestClient(app)

def test_audit():
    print("==================================================")
    print("   MATCHMYRESUME — COMPREHENSIVE AUDIT SUITE      ")
    print("==================================================")

    # TEST 1: Health check
    print("\n[AUDIT 1] Checking GET /api/health...")
    health = client.get("/api/health")
    assert health.status_code == 200
    h_data = health.json()
    assert h_data["status"] == "healthy"
    print(f" PASS: Backend is healthy (Version: {h_data['version']})")

    # TEST 2: Invalid File Uploads
    print("\n[AUDIT 2] Testing Invalid PDF Upload Handlers...")
    # 2a. Non-PDF file
    bad_file = {"resume_file": ("test.txt", b"plain text content", "text/plain")}
    res_bad = client.post("/api/analyze", files=bad_file, data={"job_description": "Valid job description requirements"})
    assert res_bad.status_code == 400
    assert "Only PDF resume documents are supported" in res_bad.json()["detail"]
    print(" PASS: Non-PDF rejected with status 400.")

    # 2b. Empty PDF bytes
    empty_bytes = b""
    bad_pdf = {"resume_file": ("empty.pdf", empty_bytes, "application/pdf")}
    res_empty = client.post("/api/analyze", files=bad_pdf, data={"job_description": "Valid job description requirements"})
    assert res_empty.status_code == 400
    print(" PASS: Empty PDF rejected with status 400.")

    # 2c. Scanned/Blank PDF (< 50 chars)
    scanned_doc = pymupdf.open()
    p = scanned_doc.new_page()
    p.insert_text((10, 10), "Hi") # Only 2 chars
    scanned_bytes = scanned_doc.tobytes()
    scanned_doc.close()
    bad_scanned = {"resume_file": ("scanned.pdf", scanned_bytes, "application/pdf")}
    res_scanned = client.post("/api/analyze", files=bad_scanned, data={"job_description": "Valid job description requirements"})
    assert res_scanned.status_code == 400
    assert "scanned image or empty" in res_scanned.json()["detail"]
    print(" PASS: Scanned/unreadable image PDF rejected with status 400.")

    # TEST 3: Invalid Job Description
    print("\n[AUDIT 3] Testing Job Description Validation...")
    doc = pymupdf.open()
    p = doc.new_page()
    p.insert_text((50, 50), "Senior Full-Stack Engineer with Python, React, FastAPI, Docker, and PostgreSQL experience.")
    valid_pdf_bytes = doc.tobytes()
    doc.close()

    res_short_jd = client.post(
        "/api/analyze",
        files={"resume_file": ("resume.pdf", valid_pdf_bytes, "application/pdf")},
        data={"job_description": "Too short"} # < 30 chars
    )
    assert res_short_jd.status_code == 400
    assert "Job description is too short" in res_short_jd.json()["detail"]
    print(" PASS: Short Job Description rejected with status 400.")

    # TEST 4: Valid Resume Analysis & Real Data Generation
    print("\n[AUDIT 4] Testing Full Resume Analysis Pipeline with Real Data...")
    resume_text = """
    Jordan Miller
    Senior Full-Stack Software Engineer
    jordan.miller@example.com | San Francisco, CA
    
    Technical Skills:
    Python, FastAPI, React.js, TypeScript, PostgreSQL, Docker, Git, REST APIs, Tailwind CSS, Problem Solving, Cross-Functional Collaboration.
    
    Professional Experience:
    Senior Software Engineer - FinScale Systems (2021 - Present)
    - Architected and deployed 15+ RESTful microservices using FastAPI and PostgreSQL.
    - Built reactive dashboard interfaces using React.js and Tailwind CSS.
    - Implemented Docker containers and CI/CD pipelines for deployment.
    - Mentored junior engineers and led agile sprint planning sessions.
    """
    doc = pymupdf.open()
    p = doc.new_page()
    p.insert_text((50, 50), resume_text)
    full_pdf_bytes = doc.tobytes()
    doc.close()

    jd_text = """
    Role: Senior Full-Stack Engineer
    Requirements:
    - 3+ years experience with Python, FastAPI, and React.js
    - Experience with PostgreSQL, Docker, Kubernetes, and AWS Cloud
    - Strong communication, problem solving, and agile collaboration
    - Nice to have: GraphQL, Redis
    """

    res_analyze = client.post(
        "/api/analyze",
        files={"resume_file": ("jordan_miller_resume.pdf", full_pdf_bytes, "application/pdf")},
        data={"job_description": jd_text}
    )
    assert res_analyze.status_code == 200
    data = res_analyze.json()

    print(f" Filename: {data['meta']['filename']}")
    print(f" Extracted Characters: {data['meta']['char_count']}")
    print(f" Match Score: {data['similarity_metrics']['match_score_percentage']}%")
    print(f" Interpretation: {data['similarity_metrics']['interpretation']}")
    print(f" Matched Skills: {data['skill_analysis']['matching_skills']}")
    print(f" Missing Skills: {data['skill_analysis']['missing_skills']}")

    assert data['similarity_metrics']['match_score_percentage'] > 0
    assert "Python" in data['skill_analysis']['matching_skills']
    assert "FastAPI" in data['skill_analysis']['matching_skills']
    assert "React.js" in data['skill_analysis']['matching_skills']
    assert "Kubernetes" in data['skill_analysis']['missing_skills']
    assert "AWS" in data['skill_analysis']['missing_skills']
    assert len(data['ai_insights']['strengths']) > 0
    assert len(data['ai_insights']['weaknesses']) > 0
    assert len(data['ai_insights']['bullet_point_improvements']) > 0
    print(" PASS: Valid analysis pipeline produced accurate, ground-truth results.")

    # TEST 5: Interactive Chat API with Resume Context
    print("\n[AUDIT 5] Testing POST /api/chat with Actual Resume Context...")
    chat_payload = {
        "question": "Which specific technical skills should I learn to bridge my gap?",
        "resume_summary": {
            "match_score": data['similarity_metrics']['match_score_percentage'],
            "matching_skills": data['skill_analysis']['matching_skills'],
            "missing_skills": data['skill_analysis']['missing_skills'],
            "strengths": data['ai_insights']['strengths'],
            "weaknesses": data['ai_insights']['weaknesses']
        }
    }
    chat_res = client.post("/api/chat", json=chat_payload)
    assert chat_res.status_code == 200
    answer = chat_res.json()["answer"]
    print(f" Question: {chat_payload['question']}")
    print(f" Answer Preview: {answer[:140]}...")
    # The answer must mention the actual missing skills
    assert any(skill in answer for skill in ["Kubernetes", "AWS", "GraphQL", "Redis"])
    print(" PASS: Chat response accurately referenced candidate's real skill gaps.")

    # TEST 6: Empty question validation
    print("\n[AUDIT 6] Testing Empty Chat Question Validation...")
    res_empty_q = client.post("/api/chat", json={"question": "   ", "resume_summary": {}})
    assert res_empty_q.status_code == 400
    print(" PASS: Empty chat question rejected with status 400.")

    print("\n==================================================")
    print("   ALL AUDIT TEST SUITE CHECKS PASSED (6/6)      ")
    print("==================================================")

if __name__ == "__main__":
    test_audit()
