import os
import json
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app.config import settings
from backend.app.services.gemini_service import generate_contextual_feedback, call_gemini_api
from backend.app.services.chat_service import answer_resume_question

def validate_gemini():
    print("=" * 80)
    print("       INDEPENDENT VALIDATION OF GOOGLE GEMINI INTEGRATION & RESILIENCE")
    print("=" * 80)
    
    # 1. Configured Model Inspection
    configured_model = settings.GEMINI_MODEL
    key_present = bool(settings.GEMINI_API_KEY)
    print(f"1. Exact Configured Model: {configured_model}")
    print(f"   API Key Configured: {key_present} (Length: {len(settings.GEMINI_API_KEY)} chars)")
    
    test_resume = """
    Marcus Vance - Full-Stack Developer
    Technical Skills: Python, FastAPI, React.js, PostgreSQL, Docker, Git.
    Experience: Built containerized web APIs and reactive frontends for e-commerce.
    """
    test_jd = "Seeking Full-Stack Engineer with Python, FastAPI, React.js, PostgreSQL, Docker, and Kubernetes."
    skill_data = {
        "matching_skills": ["Python", "FastAPI", "React.js", "PostgreSQL", "Docker", "Git"],
        "missing_skills": ["Kubernetes"],
        "additional_skills": []
    }
    similarity_score = 48.5
    
    results = {}
    
    # 2. Live API Call for Resume Recommendations
    print("\n2. Executing Real Live Gemini API Call (Resume Recommendations)...")
    try:
        live_res = call_gemini_api(
            api_key=settings.GEMINI_API_KEY,
            resume_text=test_resume,
            job_description=test_jd,
            skill_data=skill_data,
            similarity_score=similarity_score
        )
        live_source = live_res.get("source", "Unknown")
        print(f"   Source Tag: {live_source}")
        print(f"   Summary: {live_res.get('summary')[:100]}...")
        print(f"   Strengths count: {len(live_res.get('strengths', []))}")
        print(f"   Missing explanations: {len(live_res.get('missing_skill_explanations', []))}")
        print(f"   Bullet improvements: {len(live_res.get('bullet_point_improvements', []))}")
        results["live_api"] = {
            "status": "PASS" if live_source == "Google Gemini AI" else "FAIL",
            "source": live_source,
            "sample_summary": live_res.get("summary")[:120],
            "sample_improvement": live_res.get("bullet_point_improvements", [{}])[0]
        }
    except Exception as e:
        print(f"   Live API Error: {e}")
        results["live_api"] = {"status": "FAIL", "error": str(e)}

    # 3. Follow-up Chat Question
    print("\n3. Testing Follow-up Interactive Chat Question...")
    try:
        chat_answer = answer_resume_question(
            question="What is the most critical missing skill I need to learn for this job?",
            resume_summary={
                "match_score": 48.5,
                "matching_skills": ["Python", "FastAPI", "React.js", "PostgreSQL", "Docker"],
                "missing_skills": ["Kubernetes"],
                "strengths": ["Strong core stack alignment"],
                "weaknesses": ["Lacks container orchestration"]
            }
        )
        print(f"   Chat Answer Length: {len(chat_answer)} characters")
        print(f"   Answer Snippet: {chat_answer[:140]}...")
        mentions_k8s = "Kubernetes" in chat_answer or "kubernetes" in chat_answer.lower()
        print(f"   Grounded in candidate gap (mentions Kubernetes): {mentions_k8s}")
        results["chat_test"] = {
            "status": "PASS" if mentions_k8s and len(chat_answer) > 50 else "FAIL",
            "snippet": chat_answer[:150],
            "mentions_gap": mentions_k8s
        }
    except Exception as e:
        print(f"   Chat Test Error: {e}")
        results["chat_test"] = {"status": "FAIL", "error": str(e)}

    # 4. Missing API Key Test (Graceful Fallback)
    print("\n4. Testing Missing API Key Handling (Fallback)...")
    missing_res = generate_contextual_feedback(test_resume, test_jd, skill_data, similarity_score, api_key="")
    missing_source = missing_res.get("source", "Unknown")
    print(f"   Returned Source Tag: {missing_source}")
    print(f"   Fallback Summary: {missing_res.get('summary')[:100]}...")
    results["missing_key_test"] = {
        "status": "PASS" if "Fallback" in missing_source else "FAIL",
        "source": missing_source
    }

    # 5. Invalid API Key Test (Simulated 400 Bad Request)
    print("\n5. Testing Invalid API Key Handling...")
    invalid_res = generate_contextual_feedback(test_resume, test_jd, skill_data, similarity_score, api_key="AIzaSy_FAKE_INVALID_TEST_KEY")
    invalid_source = invalid_res.get("source", "Unknown")
    print(f"   Returned Source Tag: {invalid_source}")
    results["invalid_key_test"] = {
        "status": "PASS" if "Fallback" in invalid_source else "FAIL",
        "source": invalid_source
    }

    print("\n" + "=" * 80)
    print("                     GEMINI VALIDATION SUMMARY                         ")
    print("=" * 80)
    for k, v in results.items():
        print(f"  • {k:<20}: Status {v['status']}")
    print("=" * 80)
    
    with open("backend/gemini_independent_validation_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    validate_gemini()
