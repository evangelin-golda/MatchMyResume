import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
for p in [BACKEND_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi.testclient import TestClient
import pymupdf
from app.main import app
from app.config import settings

client = TestClient(app)

def test_gemini_resilience():
    print("Testing Gemini resilience with invalid/expired key...")
    # Intentionally set an invalid key to test exception catch & fallback
    settings.GEMINI_API_KEY = "AIzaSy_INVALID_KEY_TEST_RESILIENCE"

    doc = pymupdf.open()
    p = doc.new_page()
    p.insert_text((50, 50), "Senior Full-Stack Engineer with Python, FastAPI, React, Docker, and PostgreSQL experience.")
    pdf_bytes = doc.tobytes()
    doc.close()

    resp = client.post(
        "/api/analyze",
        files={"resume_file": ("resume.pdf", pdf_bytes, "application/pdf")},
        data={"job_description": "We are seeking a Python and FastAPI developer with Kubernetes and Docker skills."}
    )

    print(f"Status Code: {resp.status_code}")
    assert resp.status_code == 200, "API must not crash on Gemini error"
    data = resp.json()
    assert "summary" in data["ai_insights"]
    assert len(data["ai_insights"]["strengths"]) > 0
    print("PASS: Backend gracefully fell back to contextual synthesis without failing!")

    # Test chat resilience
    chat_resp = client.post(
        "/api/chat",
        json={
            "question": "How can I improve my score?",
            "resume_summary": {
                "match_score": 50.0,
                "matching_skills": ["Python", "FastAPI"],
                "missing_skills": ["Kubernetes"]
            }
        }
    )
    print(f"Chat Status Code: {chat_resp.status_code}")
    assert chat_resp.status_code == 200
    print(f"Chat Answer: {chat_resp.json()['answer'][:100]}...")
    print("PASS: Chat gracefully fell back to contextual responder without failing!")

    # Reset key
    settings.GEMINI_API_KEY = ""

if __name__ == "__main__":
    test_gemini_resilience()
