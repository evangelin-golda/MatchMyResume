from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os

try:
    from app.config import settings
    from app.services.pdf_service import extract_text_from_pdf
    from app.services.skill_service import compare_skills
    from app.services.ml_service import calculate_similarity_score
    from app.services.gemini_service import generate_contextual_feedback
    from app.services.chat_service import answer_resume_question
except ImportError:
    from backend.app.config import settings
    from backend.app.services.pdf_service import extract_text_from_pdf
    from backend.app.services.skill_service import compare_skills
    from backend.app.services.ml_service import calculate_similarity_score
    from backend.app.services.gemini_service import generate_contextual_feedback
    from backend.app.services.chat_service import answer_resume_question

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Backend API for MatchMyResume AI platform"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    resume_summary: Dict
    chat_history: Optional[List[Dict]] = []

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }

@app.post("/api/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1. Validate file extension and MIME
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resume documents are supported. Please upload a .pdf file."
        )
        
    # 2. Validate job description input
    clean_jd = job_description.strip()
    if len(clean_jd) < 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is too short. Please provide at least 30 characters of job requirements."
        )

    # 3. Read bytes in-memory and extract text
    pdf_bytes = await resume_file.read()
    resume_text = extract_text_from_pdf(pdf_bytes)
    
    # 4. Extract & Compare skills (NLP)
    skill_data = compare_skills(resume_text, clean_jd)
    
    # 5. Compute mathematical TF-IDF Cosine Similarity (ML)
    similarity_data = calculate_similarity_score(resume_text, clean_jd)
    match_score = similarity_data["match_score"]
    
    # 6. Generate AI recommendations & feedback (Gemini)
    ai_insights = generate_contextual_feedback(
        resume_text=resume_text,
        job_description=clean_jd,
        skill_data=skill_data,
        similarity_score=match_score
    )
    
    # Assemble comprehensive response
    return {
        "meta": {
            "filename": resume_file.filename,
            "filesize_bytes": len(pdf_bytes),
            "char_count": len(resume_text),
        },
        "similarity_metrics": {
            "match_score_percentage": match_score,
            "interpretation": similarity_data["interpretation"],
            "disclaimer": similarity_data["disclaimer"]
        },
        "skill_analysis": skill_data,
        "ai_insights": ai_insights
    }

@app.post("/api/chat")
async def chat_with_resume(request: ChatRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    answer = answer_resume_question(
        question=request.question.strip(),
        resume_summary=request.resume_summary,
        chat_history=request.chat_history
    )
    
    return {
        "question": request.question,
        "answer": answer
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
