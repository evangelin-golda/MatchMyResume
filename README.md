<div align="center">

# 🌿 MatchMyResume
### **AI-Powered Resume Analyzer & Job Matching Platform**

*Empowering job seekers, students, and professionals with mathematical precision, deep skill taxonomy, and generative career intelligence.*

---

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite_6-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styles-Tailwind_CSS_v3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Google Gemini](https://img.shields.io/badge/Generative_AI-Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn_TF--IDF-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2E7D32?style=for-the-badge)](./LICENSE)
[![System Audit](https://img.shields.io/badge/Test_Audit-95.8%25_Passing-10B981?style=for-the-badge)](./MATCHMYRESUME_TEST_REPORT.md)

[Features](#-key-features) • [Architecture](#-system-architecture) • [Accuracy Benchmarks](#-accuracy--evaluation-benchmarks) • [Quick Start](#-installation--quick-start) • [API Docs](#-api-reference)

</div>

---

## 📌 Project Overview

**MatchMyResume** is a full-stack, AI-driven web application that analyzes how well a candidate's resume matches a specific target job description. 

Unlike generic AI resume wrappers that rely solely on ungrounded language model prompts, MatchMyResume implements a **multi-tiered architecture**:
1. **In-Memory PDF Extraction Engine:** Securely parses PDF documents in RAM using PyMuPDF (`fitz`), guaranteeing zero disk persistence.
2. **Boundary-Safe NLP Skill Taxonomy:** Extracts over **500+ curated technical and soft skills** using descending-length phrase-span masking to eliminate sub-token false positives.
3. **Mathematical Text Vectorization & Scoring:** Employs Scikit-Learn TF-IDF bi-gram vectorization and cosine similarity to measure mathematical lexical overlap with transparent disclaimers.
4. **Context-Aware Generative AI:** Leverages Google Gemini to deliver Google XYZ format bullet-point rewrites (*"Accomplished [X] as measured by [Y] by doing [Z]"*).
5. **Deterministic Offline Synthesis Engine:** Automatically falls back to rule-based synthesis if API keys are missing or Google endpoints experience rate-limit spikes (HTTP 503), ensuring zero downtime.
6. **Interactive AI Career Coach:** An embedded chat assistant grounded strictly in candidate resume facts.

---

## 🎯 The Problem & The Solution

| The Job Seeker's Challenge | How MatchMyResume Solves It |
| :--- | :--- |
| **The ATS "Black Box":** Applying blindly without knowing if the resume matches role requirements. | **Transparent Similarity & Coverage:** Instant breakdown of matching skills, missing skills, and vocabulary overlap. |
| **Hidden Skill Gaps:** Not knowing which omitted qualifications are genuine deal-breakers. | **Categorized Gap Analysis:** Distinguishes core technical dependencies from supplementary skills. |
| **Weak, Passive Phrasing:** Bullet points listing generic duties without measurable impact. | **Google XYZ Bullet Point Rewriter:** Generative AI rewrites existing bullets into high-impact, quantified metrics. |
| **Data Privacy Concerns:** Uploading personal career data to cloud storage systems that retain resumes. | **Ephemeral Memory Streams:** Resumes are processed strictly in RAM buffers and discarded upon response delivery. |
| **AI Reliability Issues:** Cloud AI models crashing during peak traffic hours. | **Dual-Engine Architecture:** Seamless, transparent fallback to local rule synthesis with full attribution. |

---

## 🌿 Visual Identity: *Verdant Flow*

MatchMyResume rejects harsh dark modes and generic blue-purple gradients, opting for a calming, bespoke **botanical green / Verdant Flow** aesthetic:

- **Ambient Background:** Soft botanical sage gradient (`#E8F3DE` $\rightarrow$ `#CCE4BC`) with organic cloud diffusion.
- **Primary CTAs:** Deep forest green (`#1B3E22`) with smooth pill-shaped buttons and subtle elevation.
- **Glassmorphic Cards:** Translucent cream surfaces (`#FCFDFB` / `#F7FAF4`) with delicate borders (`rgba(27, 62, 34, 0.08)`).
- **Taxonomy Badges:** 
  - 🌿 **Matched Skills:** Spring Mint (`#D6ECD4` background, `#1B3E22` text)
  - 🍂 **Missing Skills:** Muted Rose (`#FCE8E4` background, `#7F1D1D` text)
  - 🌾 **Additional Skills:** Sage Slate (`#E2E8F0` background, `#334155` text)
- **Visual Analytics:** Interactive Recharts dynamic bar and radial charts styled to match botanical theme tokens.

---

## 🏗️ System Architecture

```
                                  +------------------------------------+
                                  |         User Web Browser           |
                                  |    (Desktop / Tablet / Mobile)     |
                                  +-----------------+------------------+
                                                    |
                                          HTTP REST (Port 8001)
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------+
| FASTAPI BACKEND MICROSERVICES                                                                     |
|                                                                                                   |
|  +---------------------------+  +---------------------------+  +-------------------------------+  |
|  |     PyMuPDF Extraction    |  |     NLP Skill Matcher     |  |     Scikit-Learn ML Engine    |  |
|  | • In-memory stream parse  |  | • 500+ Curated Skills     |  | • TF-IDF Vectorizer (1-2 gram)|  |
|  | • Zero disk persistence   |  | • Multi-word span masking |  | • Cosine Similarity Metric    |  |
|  | • Corrupt/scan validation |  | • Canonical normalization |  | • Lexical alignment scale    |  |
|  +---------------------------+  +---------------------------+  +-------------------------------+  |
|                                                                                                   |
|                                 +---------------------------+                                     |
|                                 |    AI Insights & Chat     |                                     |
|                                 | • Google Gemini REST API  |                                     |
|                                 | • gemini-flash-lite       |                                     |
|                                 | • Deterministic Fallback  |                                     |
|                                 +---------------------------+                                     |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 Repository Structure

```tree
MatchMyResume/
├── backend/
│   ├── app/                         # FastAPI application package
│   │   ├── api/routes.py            # API routes (/api/analyze, /api/chat, /api/health)
│   │   ├── services/                # Modular domain services
│   │   │   ├── pdf_service.py       # Ephemeral in-memory PyMuPDF parser
│   │   │   ├── skill_service.py     # 500+ Skill taxonomy & extraction engine
│   │   │   ├── ml_service.py        # TF-IDF vectorization & Cosine Similarity
│   │   │   ├── gemini_service.py    # Google Gemini integration & resilience fallback
│   │   │   └── chat_service.py      # Factual, resume-grounded career assistant
│   │   ├── config.py                # Pydantic environment configuration
│   │   └── main.py                  # FastAPI factory & CORS middleware
│   ├── tests/                       # Automated test suites
│   │   ├── test_backend.py          # Core unit tests (PDF, skill extraction, ML, chat)
│   │   ├── test_api_integration.py  # End-to-end FastAPI endpoint integration tests
│   │   ├── test_gemini_resilience.py# AI error handling & offline fallback tests
│   │   └── comprehensive_evaluation.py # 24-scenario empirical audit suite
│   ├── scripts/                     # Verification & benchmark utilities
│   │   ├── validate_security.py     # Repository security & secret scan
│   │   ├── validate_skill_benchmark.py # 100+ Ground-truth skill benchmark evaluation
│   │   ├── validate_ranking_quality.py # NDCG & Precision ranking benchmark
│   │   ├── validate_gemini_complete.py # Live Gemini API & resilience audit
│   │   ├── browser_validation_playwright.py # Playwright headless browser E2E test
│   │   ├── audit_existing_results.py # Test report verification tool
│   │   └── verify_all.py            # Sanity verification runner
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Backend environment variable template
├── frontend/
│   ├── src/
│   │   ├── components/              # UI components (Navbar, Footer, Charts, Chat)
│   │   ├── pages/                   # Views (LandingPage, AnalyzePage, DashboardPage, InsightsPage)
│   │   ├── context/                 # React Context (AnalysisContext state management)
│   │   ├── services/                # API client (Axios HTTP wrapper)
│   │   └── styles/                  # Tailwind CSS styling tokens
│   ├── package.json                 # Node dependencies & build scripts
│   ├── tailwind.config.js           # Verdant Flow botanical green theme configuration
│   ├── vite.config.js               # Vite build configuration & proxy setup
│   └── .env.example                 # Frontend environment variable template
├── docs/
│   └── test-reports/                # Sanitized evaluation JSON benchmarks
│       ├── evaluation_results.json
│       ├── expanded_skill_benchmark_results.json
│       ├── matching_quality_ranking_results.json
│       ├── gemini_independent_validation_results.json
│       └── security_validation_results.json
├── MATCHMYRESUME_TEST_REPORT.md     # Primary comprehensive QA audit report
├── FINAL_VALIDATION_REPORT.md       # Independent validation & verification report
├── LICENSE                          # MIT License
├── .gitignore                       # Production gitignore configuration
└── README.md                        # Project documentation
```

---

## ✨ Key Features

### 1. In-Memory Privacy-Preserving PDF Parsing
- Resumes are read directly into memory streams (`await resume_file.read()`) using **PyMuPDF (`fitz`)**.
- Rejects corrupted PDFs, zero-byte uploads, and scanned images ($<50$ extracted characters) with clear guidance.
- Zero local disk writes or database persistence.

### 2. Multi-Word Span-Masked Skill Extraction
- Pre-curated dictionary of **500+ technical frameworks, libraries, tools, and professional soft skills**.
- **Descending length phrase-span masking**: Prevents compound skills (e.g. `Tailwind CSS`) from triggering spurious sub-token false positives (standalone `CSS`), while capturing plurals (e.g. `REST APIs`, `Microservices`).
- Canonical casing normalization (`SQLite`, `gRPC`, `ChromaDB`, `PostgreSQL`, `FastAPI`).

### 3. Mathematical TF-IDF Text Vectorization
- Computes unigram and bigram term frequency-inverse document frequency distributions.
- Calculates mathematical cosine similarity distance between candidate experience and role expectations.
- Transparent disclaimer: explicitly informs the candidate that this is a **lexical distribution metric**, not an official ATS score.

### 4. Context-Aware Generative AI (Google Gemini)
- Generates structured JSON insights: Executive Summary, Key Strengths, Skill Gaps, and 3-step Career Roadmap.
- **Google XYZ Bullet Point Rewriter**: Analyzes resume bullet points and transforms them into high-impact, quantified achievements.
- Transparent source tagging: responses are explicitly attributed as `"Google Gemini AI"` or `"Offline Contextual Synthesis (Fallback)"`.

### 5. Interactive Grounded AI Career Assistant
- In-dashboard chat widget grounded strictly in the candidate's verified resume analysis.
- Answers follow-up candidate queries (e.g., *"What is my biggest gap for this role?"*) without hallucinating unearned qualifications.

---

## 📊 Accuracy & Evaluation Benchmarks

MatchMyResume has undergone independent quality and accuracy audits. The complete 24-scenario test suite is documented in [MATCHMYRESUME_TEST_REPORT.md](./MATCHMYRESUME_TEST_REPORT.md).

### Skill Extraction Metrics (Annotated Benchmark)

$$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}} = \frac{137}{137 + 5} = \mathbf{96.48\%}$$

$$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}} = \frac{137}{137 + 0} = \mathbf{100.0\%}$$

$$\text{F}_1\text{-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \mathbf{98.21\%}$$

### Information Retrieval Ranking Quality (20 Resume-JD Pairs)
Evaluated across 20 independent Resume-Job pairs against human expert relevance grading (Grade 3 = Highly Relevant, Grade 2 = Moderately Relevant, Grade 1 = Marginally Relevant, Grade 0 = Irrelevant):

| Metric | Measured Score | Ideal Target | Description |
| :--- | :---: | :---: | :--- |
| **NDCG@5** | **1.0000** | 1.0000 | Top 5 returned candidates are 100% Highly Relevant |
| **NDCG@10** | **0.9786** | 1.0000 | Normalized Discounted Cumulative Gain at rank 10 |
| **NDCG@20** | **0.9992** | 1.0000 | Overall ranking quality across all 20 pairs |
| **Precision@5** | **100.0%** | 100.0% | Percentage of top 5 pairs that are relevant ($\ge \text{Grade 2}$) |
| **Spearman ($\rho$)** | **0.9335** | 1.0000 | Statistical rank correlation between algorithm score and human grade ($p < 10^{-8}$) |

---

## 💻 Installation & Quick Start

### Prerequisites
- **Python:** v3.10 or v3.11
- **Node.js:** v18.0.0 or higher
- **VS Code** (or terminal of choice)

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/MatchMyResume.git
cd MatchMyResume
```

---

### Step 2: Backend Setup (FastAPI)

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. *(Optional)* Create and activate a virtual environment:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your local `.env` configuration:
   ```bash
   cp .env.example .env
   ```
   Configure your environment variables in `backend/.env`:
   ```env
   # Optional: Google Gemini API Key (leave empty to use offline synthesis)
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-flash-lite-latest
   PORT=8001
   ```
   *(Get a free API key at [ai.google.dev](https://ai.google.dev/))*

5. Start the FastAPI backend server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
   ```
   The backend API will run at `http://127.0.0.1:8001`. Interactive Swagger documentation will be available at `http://127.0.0.1:8001/docs`.

---

### Step 3: Frontend Setup (React + Vite)

1. Open a **second terminal window** and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure your frontend environment:
   ```bash
   cp .env.example .env
   ```
   Ensure `frontend/.env` points to the backend server:
   ```env
   VITE_API_URL=http://127.0.0.1:8001
   ```

4. Start the Vite development server:
   ```bash
   npm run dev
   ```
   Open your browser and navigate to **`http://localhost:5173`**.

---

## 🧪 Running Tests & Quality Benchmarks

Run any unit test, integration test, or empirical benchmark directly from the project root:

```bash
# 1. Run core unit tests (PDF extraction, Skill comparison, ML TF-IDF, Chat fallback)
python backend/tests/test_backend.py

# 2. Run API integration tests
python backend/tests/test_api_integration.py

# 3. Run Gemini error handling & graceful fallback tests
python backend/tests/test_gemini_resilience.py

# 4. Run repository security audit (Secret scanner, .gitignore, RAM processing)
python backend/scripts/validate_security.py

# 5. Run 100+ Ground-truth skill extraction benchmark
python backend/scripts/validate_skill_benchmark.py

# 6. Run 20-Pair Information Retrieval ranking benchmark (NDCG & Precision@K)
python backend/scripts/validate_ranking_quality.py

# 7. Run frontend production build
npm run build --prefix frontend
```

---

## 📡 API Reference

### 1. Health Check
`GET /api/health`
```json
{
  "status": "healthy",
  "app": "MatchMyResume API",
  "version": "1.0.0",
  "gemini_configured": true
}
```

### 2. Analyze Resume
`POST /api/analyze`  
*Content-Type:* `multipart/form-data`

| Parameter | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `resume_file` | File (`.pdf`) | Yes | Resume document in PDF format |
| `job_description` | String | Yes | Target job requirements (minimum 30 characters) |

**Sample Response Body:**
```json
{
  "meta": {
    "filename": "alex_rivera_resume.pdf",
    "filesize_bytes": 48210,
    "char_count": 1845
  },
  "similarity_metrics": {
    "match_score_percentage": 44.4,
    "interpretation": "Moderate Alignment",
    "disclaimer": "This score represents text similarity based on lexical distribution between your resume and the job description, not an official ATS score."
  },
  "skill_analysis": {
    "matching_skills": ["Docker", "FastAPI", "Git", "PostgreSQL", "Python", "REST APIs", "React.js"],
    "missing_skills": ["Kubernetes", "AWS"],
    "additional_skills": ["Tailwind CSS", "TypeScript"],
    "skill_coverage_percentage": 77.8,
    "total_required_skills": 9,
    "total_matched_skills": 7
  },
  "ai_insights": {
    "source": "Google Gemini AI",
    "summary": "Candidate exhibits strong core backend proficiencies...",
    "strengths": ["Demonstrated production experience with FastAPI microservices."],
    "weaknesses": ["Lacks container orchestration tools (Kubernetes)."],
    "bullet_point_improvements": [
      {
        "original": "Built microservices with FastAPI and Docker.",
        "improved": "Architected 6 containerized FastAPI microservices, reducing API response latency by 38%.",
        "explanation": "Quantifies scale and demonstrates direct business impact using Google XYZ format."
      }
    ],
    "career_recommendations": [
      "Prioritize Kubernetes hands-on container orchestration.",
      "Obtain an AWS Certified Solutions Architect credential."
    ]
  }
}
```

### 3. Context-Aware AI Chat
`POST /api/chat`  
*Content-Type:* `application/json`

```json
{
  "question": "What is the biggest skill gap on my resume for this position?",
  "resume_summary": {
    "match_score": 44.4,
    "matching_skills": ["Python", "FastAPI", "Docker"],
    "missing_skills": ["Kubernetes", "AWS"]
  }
}
```

---

## 🔒 Security & Privacy

1. **In-Memory Volatile Processing:** Candidate resumes are parsed directly from memory buffers (`await resume_file.read()`) and discarded after the HTTP response. Zero resume files are saved to the server filesystem or database.
2. **Credential Segregation:** The Google Gemini API key is managed strictly on the backend via environment variables. It is never transmitted to the browser or included in Vite client bundle builds.
3. **No Deceptive Guarantees:** MatchMyResume explicitly informs candidates that TF-IDF cosine similarity measures **vocabulary overlap and lexical distribution**, not an ATS hiring decision guarantee.
4. **Factual Prompt Grounding:** Gemini prompts strictly prohibit hallucinating degrees, institutions, or unmentioned companies.

---

## 🌐 Production Deployment Guide

### Frontend Deployment (Vercel)
1. Link your GitHub repository to [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Set **Framework Preset** to `Vite`.
4. Add the Environment Variable:
   - `VITE_API_URL` = `https://your-backend-service.onrender.com`
5. The included [frontend/vercel.json](./frontend/vercel.json) handles single-page client routing automatically.

### Backend Deployment (Render / Railway)
1. Create a new **Web Service** on [Render](https://render.com) pointing to your repository.
2. Set **Root Directory** to `backend`.
3. Set **Build Command:** `pip install -r requirements.txt`.
4. Set **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Add the Environment Variables:
   - `GEMINI_API_KEY` = `your_google_gemini_api_key`
   - `GEMINI_MODEL` = `gemini-flash-lite-latest`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](./LICENSE).

---

<div align="center">

Developed with passion by the **MatchMyResume** Team.  
*Star ⭐ this repository if you find it helpful!*

</div>
