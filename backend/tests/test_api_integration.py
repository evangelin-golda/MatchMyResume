import sys
import os

# Add backend directory and project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
for p in [BACKEND_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi.testclient import TestClient
import pymupdf
from app.main import app

def run_integration_tests():
    print("Initializing FastAPI TestClient...")
    client = TestClient(app)

    # 1. Test /api/health
    print("Testing GET /api/health...")
    health = client.get("/api/health")
    print(f"Health Status: {health.status_code}, Response: {health.json()}")
    assert health.status_code == 200

    # 2. Test POST /api/analyze with real PDF
    print("\nCreating in-memory sample PDF resume...")
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), """
    Alex Rivera
    Senior Full-Stack Engineer
    alex.rivera@example.com | San Francisco, CA
    
    Professional Summary:
    Experienced Full-Stack Developer with 4+ years of building web applications with Python, FastAPI, and React.js.
    
    Technical Skills:
    Python, JavaScript, TypeScript, React.js, FastAPI, PostgreSQL, Docker, Git, REST APIs, Tailwind CSS, Problem Solving, Teamwork.
    
    Work Experience:
    Senior Software Engineer - CloudTech Solutions (2022 - Present)
    - Architected and scaled microservices using FastAPI, Python, and PostgreSQL.
    - Developed responsive, accessible web frontends using React.js and Tailwind CSS.
    - Implemented Docker containerization and automated CI/CD deployment pipelines.
    - Collaborated with cross-functional product and engineering teams.
    """)
    pdf_bytes = doc.tobytes()
    doc.close()

    print("Testing POST /api/analyze with PDF + Job Description...")
    files = {
        "resume_file": ("alex_rivera_resume.pdf", pdf_bytes, "application/pdf")
    }
    data = {
        "job_description": """
        Position: Full-Stack Software Engineer
        Requirements:
        - Strong hands-on experience with Python, FastAPI, React.js, and TypeScript
        - Deep understanding of PostgreSQL, Docker, Kubernetes, and AWS cloud
        - Familiarity with REST APIs, CI/CD, Problem Solving, and Collaboration
        """
    }
    resp = client.post("/api/analyze", files=files, data=data)
    print(f"Analyze Status: {resp.status_code}")
    assert resp.status_code == 200
    res_data = resp.json()

    print(f"Extracted File: {res_data['meta']['filename']} ({res_data['meta']['char_count']} chars)")
    print(f"Match Score: {res_data['similarity_metrics']['match_score_percentage']}% ({res_data['similarity_metrics']['interpretation']})")
    print(f"Matching Skills ({len(res_data['skill_analysis']['matching_skills'])}): {res_data['skill_analysis']['matching_skills']}")
    print(f"Missing Skills ({len(res_data['skill_analysis']['missing_skills'])}): {res_data['skill_analysis']['missing_skills']}")
    print(f"AI Summary Preview: {res_data['ai_insights']['summary'][:120]}...")

    assert len(res_data['skill_analysis']['matching_skills']) >= 4
    assert "Kubernetes" in res_data['skill_analysis']['missing_skills']

    # 3. Test POST /api/chat with current analysis context
    print("\nTesting POST /api/chat with candidate inquiry...")
    chat_payload = {
        "question": "Which skills am I missing for this job?",
        "resume_summary": {
            "match_score": res_data['similarity_metrics']['match_score_percentage'],
            "matching_skills": res_data['skill_analysis']['matching_skills'],
            "missing_skills": res_data['skill_analysis']['missing_skills'],
            "strengths": res_data['ai_insights']['strengths'],
            "weaknesses": res_data['ai_insights']['weaknesses']
        }
    }
    chat_resp = client.post("/api/chat", json=chat_payload)
    print(f"Chat Status: {chat_resp.status_code}")
    assert chat_resp.status_code == 200
    answer = chat_resp.json()["answer"]
    print(f"Chat Answer Preview: {answer[:140]}...")
    assert "Kubernetes" in answer

    print("\nALL FastAPI ENDPOINTS VERIFIED & PASSING!")

if __name__ == "__main__":
    run_integration_tests()
