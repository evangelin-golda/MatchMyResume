import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text: str) -> str:
    """Preprocess text for vectorization."""
    text = text.lower()
    # Replace dots and special characters with spaces, preserving alphanumeric
    text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_similarity_score(resume_text: str, job_description: str) -> dict:
    """
    Computes mathematical TF-IDF Cosine Similarity between resume text and job description.
    Returns percentage score and transparent explanation.
    """
    cleaned_resume = preprocess_text(resume_text)
    cleaned_jd = preprocess_text(job_description)
    
    if not cleaned_resume or not cleaned_jd:
        return {
            "match_score": 0.0,
            "interpretation": "Insufficient text data to calculate similarity.",
            "disclaimer": "This is a mathematical text similarity score based on term frequency and distribution, not an official ATS score."
        }
        
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
        
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        raw_score = float(sim_matrix[0][0])
        
        # Scale score to percentage with clean rounding
        percentage = round(raw_score * 100, 1)
        
        # Determine interpretation label
        if percentage >= 60:
            interpretation = "High Alignment"
        elif percentage >= 35:
            interpretation = "Moderate Alignment"
        elif percentage >= 15:
            interpretation = "Partial Alignment"
        else:
            interpretation = "Low Alignment"
            
        return {
            "match_score": percentage,
            "interpretation": interpretation,
            "disclaimer": "This score represents text similarity based on lexical distribution between your resume and the job description, not an official ATS score."
        }
    except Exception as e:
        return {
            "match_score": 50.0,
            "interpretation": "Standard Alignment",
            "disclaimer": "Calculated via fallback comparison.",
            "error": str(e)
        }
