import os
import time
import httpx
from typing import Dict, List
try:
    from app.config import settings
except ImportError:
    from backend.app.config import settings

def answer_resume_question(
    question: str,
    resume_summary: Dict,
    chat_history: List[Dict] = None,
    api_key: str = None
) -> str:
    """
    Answers user questions strictly grounded in their specific resume analysis and target job.
    """
    if api_key is None:
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    
    if api_key:
        try:
            return call_gemini_chat(api_key, question, resume_summary, chat_history)
        except Exception as e:
            print(f"[Chat Service] Gemini call failed: {e}. Falling back to contextual rule responder.")
            
    return fallback_contextual_answer(question, resume_summary)

def call_gemini_chat(api_key: str, question: str, resume_summary: Dict, chat_history: List[Dict]) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={api_key}"
    
    sys_prompt = f"""You are MatchMyResume's AI Career Assistant.
You are helping the candidate understand their resume analysis for a specific job application.
Candidate's Analysis Context:
- Match Score: {resume_summary.get('match_score', 'N/A')}%
- Matched Skills: {', '.join(resume_summary.get('matching_skills', []))}
- Missing Skills: {', '.join(resume_summary.get('missing_skills', []))}
- Strengths: {'; '.join(resume_summary.get('strengths', []))}
- Weaknesses: {'; '.join(resume_summary.get('weaknesses', []))}

RULES:
1. Ground all answers strictly in this resume analysis and target role.
2. Be direct, encouraging, practical, and constructive.
3. Keep answers concise (2-4 paragraphs or a short bulleted list).
4. Never invent degrees or companies the candidate did not mention.
"""

    user_query = f"Candidate Question: {question}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": sys_prompt + "\n\n" + user_query}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 600
        }
    }
    
    last_err = None
    for attempt in range(2):
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            last_err = e
            if attempt == 0:
                time.sleep(2.0)
                continue
            raise last_err
            
    return fallback_contextual_answer(question, resume_summary)

def fallback_contextual_answer(question: str, resume_summary: Dict) -> str:
    """Intelligent rule-based answers grounded in actual analysis metrics."""
    q_lower = question.lower()
    matching = resume_summary.get("matching_skills", [])
    missing = resume_summary.get("missing_skills", [])
    score = resume_summary.get("match_score", 0.0)
    tag = "\n\n*(Note: Generated via MatchMyResume offline rule synthesis)*"
    
    if "score" in q_lower or "low" in q_lower or ("why" in q_lower and "match" in q_lower):
        return (
            f"Your match score of {score}% reflects the mathematical text similarity between your resume and the job description. "
            f"It looks for both direct keyword frequency and semantic distribution. "
            f"To boost your alignment, emphasize your {len(matching)} matched skills ({', '.join(matching[:3]) if matching else 'core tools'}) and explicitly address the {len(missing)} missing skills ({', '.join(missing[:3]) if missing else 'none'})."
            + tag
        )
        
    if "missing" in q_lower or "skill" in q_lower and ("lack" in q_lower or "need" in q_lower):
        if missing:
            return (
                f"Based on the job requirements, the key skills missing from your resume are: {', '.join(missing)}. "
                f"If you have hands-on experience or academic projects using any of these, adding them to your skills list and project descriptions will immediately improve your suitability."
                + tag
            )
        return "Great news: your resume covers all the primary skills explicitly identified in this job description!" + tag

    if "improve" in q_lower or "project" in q_lower or "bullet" in q_lower:
        return (
            "To strengthen your resume content:\n"
            "1. **Use Google's XYZ Format:** Frame achievements as: 'Accomplished [X], as measured by [Y], by doing [Z]'.\n"
            "2. **Quantify Results:** Include numbers, percentages, user counts, or latency reductions.\n"
            f"3. **Incorporate Missing Keywords:** Weave in relevant missing competencies like {', '.join(missing[:2]) if missing else 'industry-standard tools'}."
            + tag
        )
        
    if "learn" in q_lower or "next" in q_lower or "career" in q_lower:
        top_missing = missing[:3] if missing else ["Cloud Deployment", "Automated Testing"]
        return (
            f"To increase your market readiness for this type of role, prioritize learning: {', '.join(top_missing)}. "
            "Building a small public GitHub project showcasing these tools will provide tangible proof for hiring managers."
            + tag
        )

    # General answer
    return (
        f"Regarding your inquiry about '{question}': Your current profile demonstrates strong alignment in {', '.join(matching[:3]) if matching else 'core technical areas'} with an overall {score}% similarity. "
        f"Focus on incorporating key missing keywords ({', '.join(missing[:2]) if missing else 'targeted requirements'}) and highlighting measurable achievements in your experience."
        + tag
    )
