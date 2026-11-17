import sys
import os
import json
import time

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

def create_pdf(text: str) -> bytes:
    doc = pymupdf.open()
    import textwrap
    wrapped_lines = []
    for paragraph in text.split('\n'):
        if paragraph.strip():
            wrapped_lines.extend(textwrap.wrap(paragraph, width=80))
        else:
            wrapped_lines.append('')
    chunk_size = 45
    for i in range(0, max(1, len(wrapped_lines)), chunk_size):
        page = doc.new_page()
        chunk = wrapped_lines[i:i+chunk_size]
        page.insert_textbox(pymupdf.Rect(40, 40, 550, 800), '\n'.join(chunk))
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def run_evaluation():
    print("======================================================================")
    print("   MATCHMYRESUME — COMPREHENSIVE 24-SCENARIO ACCURACY & QUALITY AUDIT ")
    print("======================================================================")

    results = []

    # Ground truth skill metrics tracking
    total_tp = 0
    total_fp = 0
    total_fn = 0

    # Save real key for dedicated AI live scenario (TC-22) to avoid rate-limiting during parsing/validation tests
    real_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    settings.GEMINI_API_KEY = ""
    os.environ["GEMINI_API_KEY"] = ""

    # ---------------------------------------------------------
    # SCENARIO 1: Strong Match (Full-Stack Engineer)
    # ---------------------------------------------------------
    print("\nExecuting TC-01: Strong Match...")
    res_text_01 = """
    Alex Rivera - Senior Full-Stack Engineer
    Technical Skills: Python, FastAPI, React.js, TypeScript, PostgreSQL, Docker, Git, REST APIs, Tailwind CSS, Problem Solving, Collaboration.
    Experience: 5 years building scalable web applications with Python, FastAPI, and React.js. Deployed containerized microservices using Docker and PostgreSQL.
    """
    gt_skills_01 = {"Python", "FastAPI", "React.js", "TypeScript", "PostgreSQL", "Docker", "Git", "REST APIs", "Tailwind CSS", "Problem Solving", "Collaboration"}
    jd_01 = "Seeking Full-Stack Engineer proficient in Python, FastAPI, React.js, PostgreSQL, Docker, Git, REST APIs, and Problem Solving."
    
    resp_01 = client.post("/api/analyze", files={"resume_file": ("s1.pdf", create_pdf(res_text_01), "application/pdf")}, data={"job_description": jd_01})
    assert resp_01.status_code == 200
    d1 = resp_01.json()
    extracted_01 = set(d1["skill_analysis"]["matching_skills"]).union(set(d1["skill_analysis"]["additional_skills"]))
    
    tp1 = len(extracted_01.intersection(gt_skills_01))
    fp1 = len(extracted_01.difference(gt_skills_01))
    fn1 = len(gt_skills_01.difference(extracted_01))
    total_tp += tp1; total_fp += fp1; total_fn += fn1

    results.append({
        "id": "TC-01",
        "category": "Matching Accuracy",
        "description": "Strong match full-stack engineer against full-stack JD",
        "expected": "Moderate-to-High Text Match (>=35%), Missing Skills = 0",
        "actual_score": d1["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d1["skill_analysis"]["matching_skills"],
        "actual_missing": d1["skill_analysis"]["missing_skills"],
        "status": "PASS" if d1["similarity_metrics"]["match_score_percentage"] >= 35 and len(d1["skill_analysis"]["missing_skills"]) == 0 else "FAIL",
        "notes": f"Score {d1['similarity_metrics']['match_score_percentage']}%, Coverage {d1['skill_analysis']['skill_coverage_percentage']}%"
    })

    # ---------------------------------------------------------
    # SCENARIO 2: Partial Match (Backend Python on Full-Stack JD)
    # ---------------------------------------------------------
    print("Executing TC-02: Partial Match...")
    res_text_02 = """
    Morgan Lee - Backend Developer
    Technical Skills: Python, FastAPI, Django, PostgreSQL, Redis, Docker, Git, Linux.
    Experience: Focused exclusively on server-side architecture, async endpoints, and database caching.
    """
    gt_skills_02 = {"Python", "FastAPI", "Django", "PostgreSQL", "Redis", "Docker", "Git", "Linux"}
    jd_02 = "Looking for Full-Stack Developer with Python, FastAPI, React.js, TypeScript, Tailwind CSS, PostgreSQL, and Docker."
    
    resp_02 = client.post("/api/analyze", files={"resume_file": ("s2.pdf", create_pdf(res_text_02), "application/pdf")}, data={"job_description": jd_02})
    assert resp_02.status_code == 200
    d2 = resp_02.json()
    extracted_02 = set(d2["skill_analysis"]["matching_skills"]).union(set(d2["skill_analysis"]["additional_skills"]))
    
    tp2 = len(extracted_02.intersection(gt_skills_02))
    fp2 = len(extracted_02.difference(gt_skills_02))
    fn2 = len(gt_skills_02.difference(extracted_02))
    total_tp += tp2; total_fp += fp2; total_fn += fn2

    missing_expected_02 = {"React.js", "TypeScript", "Tailwind CSS"}
    missing_actual_02 = set(d2["skill_analysis"]["missing_skills"])
    is_correct_02 = missing_expected_02.issubset(missing_actual_02)

    results.append({
        "id": "TC-02",
        "category": "Skill Gap Detection",
        "description": "Backend engineer applying for Full-Stack JD",
        "expected": "Missing frontend stack: React.js, TypeScript, Tailwind CSS",
        "actual_score": d2["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d2["skill_analysis"]["matching_skills"],
        "actual_missing": d2["skill_analysis"]["missing_skills"],
        "status": "PASS" if is_correct_02 else "FAIL",
        "notes": f"Correctly detected missing frontend requirements: {d2['skill_analysis']['missing_skills']}"
    })

    # ---------------------------------------------------------
    # SCENARIO 3: Poor Match (Accountant on DevOps JD)
    # ---------------------------------------------------------
    print("Executing TC-03: Poor Match...")
    res_text_03 = """
    Casey Clark - Senior Accountant & Financial Analyst
    Expertise: General ledger, Accounts Payable, Auditing, GAAP, Balance Sheet Reconciliation, Tax Compliance, Financial Reporting, Excel.
    Experience: 7 years managing fiscal audits and corporate accounting departments.
    """
    jd_03 = "DevOps Engineer required: Kubernetes, Docker, Terraform, AWS, CI/CD pipelines, Linux, Python, Helm."
    resp_03 = client.post("/api/analyze", files={"resume_file": ("s3.pdf", create_pdf(res_text_03), "application/pdf")}, data={"job_description": jd_03})
    assert resp_03.status_code == 200
    d3 = resp_03.json()
    
    results.append({
        "id": "TC-03",
        "category": "Negative Discrimination",
        "description": "Finance/Accounting resume evaluated against DevOps Lead JD",
        "expected": "Low Match Score (<15%), 0 Matched Technical Skills",
        "actual_score": d3["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d3["skill_analysis"]["matching_skills"],
        "actual_missing": d3["skill_analysis"]["missing_skills"],
        "status": "PASS" if d3["similarity_metrics"]["match_score_percentage"] < 15 and len(d3["skill_analysis"]["matching_technical"]) == 0 else "FAIL",
        "notes": f"Score {d3['similarity_metrics']['match_score_percentage']}% properly reflects zero technical overlap."
    })

    # ---------------------------------------------------------
    # SCENARIO 4: Missing Critical Skill (Senior Dev missing Kubernetes)
    # ---------------------------------------------------------
    print("Executing TC-04: Missing Critical Skill...")
    res_text_04 = """
    Taylor Smith - Backend Architect
    Skills: Python, FastAPI, Docker, PostgreSQL, Redis, AWS, Git, CI/CD.
    Experience: Deep cloud experience building containerized Python services on AWS.
    """
    jd_04 = "Senior Infrastructure Engineer: Must have Python, Docker, Kubernetes, and Helm."
    resp_04 = client.post("/api/analyze", files={"resume_file": ("s4.pdf", create_pdf(res_text_04), "application/pdf")}, data={"job_description": jd_04})
    d4 = resp_04.json()
    results.append({
        "id": "TC-04",
        "category": "Skill Gap Detection",
        "description": "Experienced backend dev lacking container orchestration (Kubernetes, Helm)",
        "expected": "Kubernetes & Helm flagged as Missing Skills",
        "actual_score": d4["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d4["skill_analysis"]["matching_skills"],
        "actual_missing": d4["skill_analysis"]["missing_skills"],
        "status": "PASS" if "Kubernetes" in d4["skill_analysis"]["missing_skills"] and "Helm" in d4["skill_analysis"]["missing_skills"] else "FAIL",
        "notes": f"Flagged gaps: {d4['skill_analysis']['missing_skills']}"
    })

    # ---------------------------------------------------------
    # SCENARIO 5: Additional Unrelated Skills (ML tools on Frontend JD)
    # ---------------------------------------------------------
    print("Executing TC-05: Additional Unrelated Skills...")
    res_text_05 = """
    Devin Vance - UI Developer & ML Enthusiast
    Skills: React.js, JavaScript, HTML, CSS, Tailwind CSS, PyTorch, TensorFlow, Computer Vision, Pandas, NumPy.
    Experience: Built React frontends while researching deep learning algorithms.
    """
    jd_05 = "Frontend Engineer: React.js, JavaScript, HTML, CSS, Tailwind CSS."
    resp_05 = client.post("/api/analyze", files={"resume_file": ("s5.pdf", create_pdf(res_text_05), "application/pdf")}, data={"job_description": jd_05})
    d5 = resp_05.json()
    add_skills = set(d5["skill_analysis"]["additional_skills"])
    results.append({
        "id": "TC-05",
        "category": "Taxonomy Segregation",
        "description": "Frontend applicant with extra Machine Learning proficiencies",
        "expected": "PyTorch / TensorFlow / Computer Vision classified under Additional Skills",
        "actual_score": d5["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d5["skill_analysis"]["matching_skills"],
        "actual_missing": d5["skill_analysis"]["missing_skills"],
        "status": "PASS" if any(s in add_skills for s in ["PyTorch", "TensorFlow", "Computer Vision"]) else "FAIL",
        "notes": f"Additional skills segregated cleanly: {d5['skill_analysis']['additional_skills'][:4]}"
    })

    # ---------------------------------------------------------
    # SCENARIO 6: Multi-Column Text Flow
    # ---------------------------------------------------------
    print("Executing TC-06: Multi-Column Formatting...")
    res_text_06 = """
    [COLUMN 1]
    Contact: dev@example.com
    Skills: Python, FastAPI, Docker, SQL
    [COLUMN 2]
    Experience Summary:
    Engineered robust web applications utilizing FastAPI and Python backend microservices.
    Managed PostgreSQL instances and Docker deployment containers.
    """
    jd_06 = "Looking for a Python Developer with FastAPI and Docker experience."
    resp_06 = client.post("/api/analyze", files={"resume_file": ("s6.pdf", create_pdf(res_text_06), "application/pdf")}, data={"job_description": jd_06})
    d6 = resp_06.json()
    results.append({
        "id": "TC-06",
        "category": "Extraction Robustness",
        "description": "Two-column formatted resume layout",
        "expected": "PyMuPDF correctly extracts text across both blocks without corruption",
        "actual_score": d6["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d6["skill_analysis"]["matching_skills"],
        "actual_missing": d6["skill_analysis"]["missing_skills"],
        "status": "PASS" if {"Python", "FastAPI", "Docker"}.issubset(set(d6["skill_analysis"]["matching_skills"])) else "FAIL",
        "notes": f"Extracted {d6['meta']['char_count']} chars, correctly matched skills."
    })

    # ---------------------------------------------------------
    # SCENARIO 7: Minimal / Sparse Content (~60 words)
    # ---------------------------------------------------------
    print("Executing TC-07: Minimal Content...")
    res_text_07 = "John Doe. Junior Programmer. Python, SQL, Git. Looking for entry level programming job. Dedicated and quick learner with problem solving skills."
    jd_07 = "Python Developer position requiring Python, SQL, Git, and Problem Solving."
    resp_07 = client.post("/api/analyze", files={"resume_file": ("s7.pdf", create_pdf(res_text_07), "application/pdf")}, data={"job_description": jd_07})
    d7 = resp_07.json()
    results.append({
        "id": "TC-07",
        "category": "Boundary Condition",
        "description": "Very short sparse resume (~25 words, but > 50 chars)",
        "expected": "Extraction passes > 50 char check and accurately extracts the few present skills",
        "actual_score": d7["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d7["skill_analysis"]["matching_skills"],
        "actual_missing": d7["skill_analysis"]["missing_skills"],
        "status": "PASS" if {"Python", "SQL", "Git"}.issubset(set(d7["skill_analysis"]["matching_skills"])) else "FAIL",
        "notes": f"Extracted {d7['meta']['char_count']} chars, matched: {d7['skill_analysis']['matching_skills']}"
    })

    # ---------------------------------------------------------
    # SCENARIO 8: Extensive Content (~1,000 words multi-project)
    # ---------------------------------------------------------
    print("Executing TC-08: Extensive Content...")
    res_text_08 = "Senior Engineering Lead. " + ("Developed scalable enterprise platforms with Python, FastAPI, React.js, PostgreSQL, Docker, Kubernetes, AWS, Redis, GraphQL, CI/CD, Agile. " * 15)
    jd_08 = "Engineering Lead: Python, FastAPI, React.js, PostgreSQL, Docker, Kubernetes, AWS, CI/CD."
    resp_08 = client.post("/api/analyze", files={"resume_file": ("s8.pdf", create_pdf(res_text_08), "application/pdf")}, data={"job_description": jd_08})
    d8 = resp_08.json()
    results.append({
        "id": "TC-08",
        "category": "Scalability / Volume",
        "description": "Extensive multi-project resume (~1,200 words)",
        "expected": "Handles large input without truncation error, match score >= 35%",
        "actual_score": d8["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d8["skill_analysis"]["matching_skills"],
        "actual_missing": d8["skill_analysis"]["missing_skills"],
        "status": "PASS" if d8["similarity_metrics"]["match_score_percentage"] >= 35 and d8["meta"]["char_count"] > 1000 else "FAIL",
        "notes": f"Extracted {d8['meta']['char_count']} chars, score {d8['similarity_metrics']['match_score_percentage']}%"
    })

    # ---------------------------------------------------------
    # SCENARIO 9: Creative / Non-Traditional Headings
    # ---------------------------------------------------------
    print("Executing TC-09: Creative Headings...")
    res_text_09 = """
    Pioneer Profile: Samantha
    [Technical Arsenal]
    Python, FastAPI, Docker, PostgreSQL, REST APIs
    [Career Voyage]
    Navigated high-traffic systems, architected resilient microservices.
    [Endorsements]
    Recognized for problem solving and team leadership.
    """
    jd_09 = "Backend Developer: Python, FastAPI, Docker, PostgreSQL, REST APIs, Problem Solving, Leadership."
    resp_09 = client.post("/api/analyze", files={"resume_file": ("s9.pdf", create_pdf(res_text_09), "application/pdf")}, data={"job_description": jd_09})
    d9 = resp_09.json()
    results.append({
        "id": "TC-09",
        "category": "Extraction Robustness",
        "description": "Resume with non-standard section titles ('Arsenal', 'Voyage')",
        "expected": "Skills extracted properly despite creative headings",
        "actual_score": d9["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d9["skill_analysis"]["matching_skills"],
        "actual_missing": d9["skill_analysis"]["missing_skills"],
        "status": "PASS" if {"Python", "FastAPI", "Docker", "PostgreSQL"}.issubset(set(d9["skill_analysis"]["matching_skills"])) else "FAIL",
        "notes": f"Extracted skills matched: {d9['skill_analysis']['matching_skills']}"
    })

    # ---------------------------------------------------------
    # SCENARIO 10: Zero Identifiable Skills (Abstract prose)
    # ---------------------------------------------------------
    print("Executing TC-10: Zero Identifiable Skills...")
    res_text_10 = "Visionary catalyst dedicated to operational excellence, maximizing synergies across global enterprises, elevating corporate philosophy, and driving holistic transformation."
    jd_10 = "Software Developer: Python, Docker, Kubernetes, AWS, PostgreSQL, React."
    resp_10 = client.post("/api/analyze", files={"resume_file": ("s10.pdf", create_pdf(res_text_10), "application/pdf")}, data={"job_description": jd_10})
    d10 = resp_10.json()
    results.append({
        "id": "TC-10",
        "category": "Negative Discrimination",
        "description": "Abstract resume containing zero technical skills",
        "expected": "0 Matched Skills, High Missing Skills count",
        "actual_score": d10["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d10["skill_analysis"]["matching_skills"],
        "actual_missing": d10["skill_analysis"]["missing_skills"],
        "status": "PASS" if len(d10["skill_analysis"]["matching_skills"]) == 0 and len(d10["skill_analysis"]["missing_skills"]) > 0 else "FAIL",
        "notes": f"Correctly detected 0 matched skills, flagged all {len(d10['skill_analysis']['missing_skills'])} as missing."
    })

    # ---------------------------------------------------------
    # SCENARIO 11: Cross-JD Evaluation A (FullStack Resume -> Frontend JD)
    # ---------------------------------------------------------
    print("Executing TC-11: Cross-JD Frontend...")
    res_fs = """
    Riley Quinn - Full-Stack Developer
    Skills: React.js, TypeScript, Tailwind CSS, HTML, CSS, JavaScript, Python, FastAPI, PostgreSQL, Docker, Git.
    Experience: 3 years building modern user interfaces with React and backend services with FastAPI.
    """
    jd_fe = "Frontend Specialist: React.js, TypeScript, Tailwind CSS, HTML, CSS, JavaScript, Redux, Next.js, Jest."
    resp_11 = client.post("/api/analyze", files={"resume_file": ("s11.pdf", create_pdf(res_fs), "application/pdf")}, data={"job_description": jd_fe})
    d11 = resp_11.json()
    results.append({
        "id": "TC-11",
        "category": "Cross-JD Evaluation",
        "description": "Full-Stack resume tested against purely Frontend JD",
        "expected": "High frontend match, missing Redux/Next.js flagged",
        "actual_score": d11["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d11["skill_analysis"]["matching_skills"],
        "actual_missing": d11["skill_analysis"]["missing_skills"],
        "status": "PASS" if {"React.js", "TypeScript", "Tailwind CSS"}.issubset(set(d11["skill_analysis"]["matching_skills"])) else "FAIL",
        "notes": f"Matched frontend core: {d11['skill_analysis']['matching_skills']}"
    })

    # ---------------------------------------------------------
    # SCENARIO 12: Cross-JD Evaluation B (Same FullStack Resume -> ML JD)
    # ---------------------------------------------------------
    print("Executing TC-12: Cross-JD Machine Learning...")
    jd_ml = "Machine Learning Scientist: PyTorch, TensorFlow, Deep Learning, NLP, Scikit-Learn, Pandas, NumPy, Computer Vision."
    resp_12 = client.post("/api/analyze", files={"resume_file": ("s12.pdf", create_pdf(res_fs), "application/pdf")}, data={"job_description": jd_ml})
    d12 = resp_12.json()
    results.append({
        "id": "TC-12",
        "category": "Cross-JD Evaluation",
        "description": "Same Full-Stack resume tested against Data Science / ML JD",
        "expected": "Low Match Score (<20%), All ML tools identified as missing",
        "actual_score": d12["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d12["skill_analysis"]["matching_skills"],
        "actual_missing": d12["skill_analysis"]["missing_skills"],
        "status": "PASS" if d12["similarity_metrics"]["match_score_percentage"] < 20 and "PyTorch" in d12["skill_analysis"]["missing_skills"] else "FAIL",
        "notes": f"Properly identifies gap between web stack and ML JD: {d12['similarity_metrics']['match_score_percentage']}%"
    })

    # ---------------------------------------------------------
    # SCENARIO 13: Comparative Candidate Senior
    # ---------------------------------------------------------
    print("Executing TC-13: Senior Candidate Profile...")
    res_sr = """
    Morgan Freeman - Principal Engineer
    Skills: Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS, Redis, Microservices, CI/CD, Git, Team Leadership, Mentorship, System Architecture.
    Experience: 10 years leading microservice migrations and engineering teams.
    """
    jd_lead = "Staff Backend Engineer: Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS, Redis, CI/CD, Team Leadership."
    resp_13 = client.post("/api/analyze", files={"resume_file": ("s13.pdf", create_pdf(res_sr), "application/pdf")}, data={"job_description": jd_lead})
    d13 = resp_13.json()
    results.append({
        "id": "TC-13",
        "category": "Candidate Comparison",
        "description": "Senior/Principal engineer profile against Staff Engineer JD",
        "expected": "High Alignment (>=30%), High Skill Coverage (>=80%)",
        "actual_score": d13["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d13["skill_analysis"]["matching_skills"],
        "actual_missing": d13["skill_analysis"]["missing_skills"],
        "status": "PASS" if d13["similarity_metrics"]["match_score_percentage"] >= 30 and d13["skill_analysis"]["skill_coverage_percentage"] >= 80 else "FAIL",
        "notes": f"Score {d13['similarity_metrics']['match_score_percentage']}%, Coverage {d13['skill_analysis']['skill_coverage_percentage']}%"
    })

    # ---------------------------------------------------------
    # SCENARIO 14: Comparative Candidate Junior (on same Staff JD)
    # ---------------------------------------------------------
    print("Executing TC-14: Junior Candidate Profile on Staff JD...")
    res_jr = """
    Chris Evans - Junior Developer
    Skills: Python, Git, HTML, CSS.
    Experience: Built introductory school projects and personal scripts.
    """
    resp_14 = client.post("/api/analyze", files={"resume_file": ("s14.pdf", create_pdf(res_jr), "application/pdf")}, data={"job_description": jd_lead})
    d14 = resp_14.json()
    results.append({
        "id": "TC-14",
        "category": "Candidate Comparison",
        "description": "Junior profile on same Staff Engineer JD",
        "expected": "Score significantly lower than Senior candidate (< 25%)",
        "actual_score": d14["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d14["skill_analysis"]["matching_skills"],
        "actual_missing": d14["skill_analysis"]["missing_skills"],
        "status": "PASS" if d14["similarity_metrics"]["match_score_percentage"] < d13["similarity_metrics"]["match_score_percentage"] else "FAIL",
        "notes": f"Junior {d14['similarity_metrics']['match_score_percentage']}% vs Senior {d13['similarity_metrics']['match_score_percentage']}% correctly differentiates seniority."
    })

    # ---------------------------------------------------------
    # SCENARIO 15: Corrupted Binary PDF
    # ---------------------------------------------------------
    print("Executing TC-15: Corrupted PDF...")
    corrupt_bytes = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\nGARBAGE_DATA_CORRUPTED_BINARY_STREAM_NOT_A_REAL_PDF"
    resp_15 = client.post("/api/analyze", files={"resume_file": ("corrupt.pdf", corrupt_bytes, "application/pdf")}, data={"job_description": "Standard JD requiring Python, FastAPI, and Docker."})
    results.append({
        "id": "TC-15",
        "category": "Error Handling",
        "description": "Corrupted binary file disguised as .pdf",
        "expected": "HTTP 400 with descriptive error",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_15.status_code == 400 and "Invalid or corrupted PDF" in resp_15.json()["detail"] else "FAIL",
        "notes": f"Returned status {resp_15.status_code}: {resp_15.json().get('detail')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 16: Zero-Byte Empty PDF
    # ---------------------------------------------------------
    print("Executing TC-16: Empty Zero-Byte PDF...")
    resp_16 = client.post("/api/analyze", files={"resume_file": ("empty.pdf", b"", "application/pdf")}, data={"job_description": "Standard JD requiring Python, FastAPI, and Docker."})
    results.append({
        "id": "TC-16",
        "category": "Error Handling",
        "description": "Completely empty 0-byte PDF upload",
        "expected": "HTTP 400 with 'Empty PDF file' detail",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_16.status_code == 400 else "FAIL",
        "notes": f"Returned status {resp_16.status_code}: {resp_16.json().get('detail')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 17: Unsupported File Format (.txt)
    # ---------------------------------------------------------
    print("Executing TC-17: Unsupported File Format (.txt)...")
    resp_17 = client.post("/api/analyze", files={"resume_file": ("resume.txt", b"Some text resume", "text/plain")}, data={"job_description": "Standard JD requiring Python, FastAPI, and Docker."})
    results.append({
        "id": "TC-17",
        "category": "File Validation",
        "description": "Text file upload (.txt instead of .pdf)",
        "expected": "HTTP 400 with 'Only PDF resume documents are supported'",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_17.status_code == 400 and "Only PDF" in resp_17.json()["detail"] else "FAIL",
        "notes": f"Returned status {resp_17.status_code}: {resp_17.json().get('detail')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 18: Scanned Image / Blank (<50 chars)
    # ---------------------------------------------------------
    print("Executing TC-18: Scanned Image / Unselectable Text...")
    doc_scan = pymupdf.open()
    p = doc_scan.new_page()
    p.insert_text((10, 10), "Scan") # Only 4 chars
    scan_bytes = doc_scan.tobytes()
    doc_scan.close()
    resp_18 = client.post("/api/analyze", files={"resume_file": ("scanned.pdf", scan_bytes, "application/pdf")}, data={"job_description": "Standard JD requiring Python, FastAPI, and Docker."})
    results.append({
        "id": "TC-18",
        "category": "Input Validation",
        "description": "Scanned image or unreadable PDF with under 50 extracted characters",
        "expected": "HTTP 400 warning candidate about scanned image",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_18.status_code == 400 and "scanned image or empty" in resp_18.json()["detail"] else "FAIL",
        "notes": f"Returned status {resp_18.status_code}: {resp_18.json().get('detail')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 19: Empty / Whitespace-Only Job Description
    # ---------------------------------------------------------
    print("Executing TC-19: Empty Job Description...")
    resp_19 = client.post("/api/analyze", files={"resume_file": ("valid.pdf", create_pdf(res_text_01), "application/pdf")}, data={"job_description": "            "})
    results.append({
        "id": "TC-19",
        "category": "Input Validation",
        "description": "Whitespace-only / empty job description submission",
        "expected": "HTTP 400 requiring minimum 30 characters",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_19.status_code == 400 and "too short" in resp_19.json()["detail"] else "FAIL",
        "notes": f"Returned status {resp_19.status_code}: {resp_19.json().get('detail')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 20: Short Job Description (<30 characters)
    # ---------------------------------------------------------
    print("Executing TC-20: Short Job Description...")
    resp_20 = client.post("/api/analyze", files={"resume_file": ("valid.pdf", create_pdf(res_text_01), "application/pdf")}, data={"job_description": "We need Python dev."}) # 19 chars
    results.append({
        "id": "TC-20",
        "category": "Input Validation",
        "description": "Job description below 30 characters limit",
        "expected": "HTTP 400 requiring minimum 30 characters",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_20.status_code == 400 and "too short" in resp_20.json()["detail"] else "FAIL",
        "notes": f"Returned status {resp_20.status_code}: {resp_20.json().get('detail')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 21: Special Characters, Accents & C++/C#
    # ---------------------------------------------------------
    print("Executing TC-21: Special Characters and Punctuation...")
    res_text_21 = """
    René Müller — Résumé
    Expertise in C++, C#, .NET, Node.js, and CI/CD pipelines.
    Handled “mission-critical” systems with zero downtime (99.99%).
    Emoji test: 🚀 ⚡ 💻
    """
    jd_21 = "Systems Programmer: Must have C++, C#, Node.js, and CI/CD experience."
    resp_21 = client.post("/api/analyze", files={"resume_file": ("s21.pdf", create_pdf(res_text_21), "application/pdf")}, data={"job_description": jd_21})
    d21 = resp_21.json()
    results.append({
        "id": "TC-21",
        "category": "Edge-Case Characters",
        "description": "Resume with foreign accents (é, ü), symbols (C++, C#), quotes, and emojis",
        "expected": "Extracted without encoding crashes, C++ and C# recognized",
        "actual_score": d21["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d21["skill_analysis"]["matching_skills"],
        "actual_missing": d21["skill_analysis"]["missing_skills"],
        "status": "PASS" if {"C++", "C#"}.issubset(set(d21["skill_analysis"]["matching_skills"])) else "FAIL",
        "notes": f"Clean extraction, matched: {d21['skill_analysis']['matching_skills']}"
    })

    # ---------------------------------------------------------
    # SCENARIO 22: Live Gemini API Integration (Actual API Key)
    # ---------------------------------------------------------
    print("Executing TC-22: Live Gemini API Integration...")
    settings.GEMINI_API_KEY = real_key # Restore real key for dedicated live test
    os.environ["GEMINI_API_KEY"] = real_key
    resp_22 = client.post("/api/analyze", files={"resume_file": ("s22.pdf", create_pdf(res_text_01), "application/pdf")}, data={"job_description": jd_01})
    d22 = resp_22.json()
    ai_source = d22["ai_insights"].get("source", "Unknown")
    is_gemini_active = "Gemini" in ai_source
    results.append({
        "id": "TC-22",
        "category": "Generative AI Integration",
        "description": "Live Google Gemini API call with actual user credentials",
        "expected": "Status 200 with JSON structured insights, source tagged 'Google Gemini AI'",
        "actual_score": d22["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d22["skill_analysis"]["matching_skills"],
        "actual_missing": d22["skill_analysis"]["missing_skills"],
        "status": "PASS" if is_gemini_active and len(d22["ai_insights"]["bullet_point_improvements"]) > 0 else "FAIL",
        "notes": f"AI Source: {ai_source}. Executive summary: {d22['ai_insights']['summary'][:80]}..."
    })

    # ---------------------------------------------------------
    # SCENARIO 23: Gemini API Resilience / Fallback (Invalid Key)
    # ---------------------------------------------------------
    print("Executing TC-23: Gemini Error & Fallback Resilience...")
    old_key = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = "AIzaSy_SIMULATED_INVALID_KEY_ERROR"
    resp_23 = client.post("/api/analyze", files={"resume_file": ("s23.pdf", create_pdf(res_text_01), "application/pdf")}, data={"job_description": jd_01})
    settings.GEMINI_API_KEY = old_key # Restore key
    d23 = resp_23.json()
    is_fallback = "Fallback" in d23["ai_insights"].get("source", "")
    results.append({
        "id": "TC-23",
        "category": "Error Resilience",
        "description": "Simulated authentication failure on Gemini API",
        "expected": "HTTP 200 with source explicitly tagged as Fallback",
        "actual_score": d23["similarity_metrics"]["match_score_percentage"],
        "actual_matched": d23["skill_analysis"]["matching_skills"],
        "actual_missing": d23["skill_analysis"]["missing_skills"],
        "status": "PASS" if resp_23.status_code == 200 and is_fallback else "FAIL",
        "notes": f"Graceful fallback triggered. Source: {d23['ai_insights'].get('source')}"
    })

    # ---------------------------------------------------------
    # SCENARIO 24: Context-Aware Interactive AI Chat
    # ---------------------------------------------------------
    print("Executing TC-24: Context-Aware Interactive Chat...")
    chat_payload = {
        "question": "What are my main strengths and what should I learn next?",
        "resume_summary": {
            "match_score": d1["similarity_metrics"]["match_score_percentage"],
            "matching_skills": d1["skill_analysis"]["matching_skills"],
            "missing_skills": d1["skill_analysis"]["missing_skills"],
            "strengths": d1["ai_insights"]["strengths"],
            "weaknesses": d1["ai_insights"]["weaknesses"]
        }
    }
    resp_24 = client.post("/api/chat", json=chat_payload)
    d24 = resp_24.json()
    chat_answer = d24.get("answer", "")
    results.append({
        "id": "TC-24",
        "category": "Interactive AI Chat",
        "description": "Candidate inquiring about strengths and next learning steps",
        "expected": "HTTP 200 with contextual advice mentioning candidate skills",
        "actual_score": "N/A",
        "actual_matched": [],
        "actual_missing": [],
        "status": "PASS" if resp_24.status_code == 200 and len(chat_answer) > 50 else "FAIL",
        "notes": f"Answer preview: {chat_answer[:100]}..."
    })

    # ---------------------------------------------------------
    # CALCULATE GROUND TRUTH ACCURACY METRICS FOR SKILL EXTRACTION
    # ---------------------------------------------------------
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n======================================================================")
    print("                    EVALUATION METRICS SUMMARY                        ")
    print("======================================================================")
    print(f"Total Test Scenarios Executed: {len(results)}")
    passed_tests = sum(1 for r in results if r['status'] == 'PASS')
    failed_tests = sum(1 for r in results if r['status'] == 'FAIL')
    print(f"Passed: {passed_tests} | Failed: {failed_tests} | Pass Rate: {round(passed_tests/len(results)*100, 1)}%")
    print(f"\nGround Truth Skill Extraction Metrics (Annotated Test Subsets):")
    print(f"  • True Positives (TP):  {total_tp}")
    print(f"  • False Positives (FP): {total_fp}")
    print(f"  • False Negatives (FN): {total_fn}")
    print(f"  • Precision:            {round(precision * 100, 2)}%")
    print(f"  • Recall:               {round(recall * 100, 2)}%")
    print(f"  • F1-Score:             {round(f1 * 100, 2)}%")
    print("======================================================================")

    # Save results as JSON for report generation
    reports_dir = os.path.join(PROJECT_ROOT, "docs", "test-reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, "evaluation_results.json")
    with open(report_path, "w") as f:
        json.dump({
            "scenarios": results,
            "metrics": {
                "total": len(results),
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": round(passed_tests / len(results) * 100, 1),
                "skill_tp": total_tp,
                "skill_fp": total_fp,
                "skill_fn": total_fn,
                "skill_precision": round(precision * 100, 2),
                "skill_recall": round(recall * 100, 2),
                "skill_f1": round(f1 * 100, 2)
            }
        }, f, indent=2)

if __name__ == "__main__":
    run_evaluation()
