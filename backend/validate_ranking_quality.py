import math
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app.services.ml_service import calculate_similarity_score
from backend.app.services.skill_service import compare_skills

# ==============================================================================
# 20 RESUME - JOB DESCRIPTION PAIRS BENCHMARK
# Human Rubric:
#   3 = Highly Relevant (Strong Match: Primary stack, frameworks, tools align)
#   2 = Moderately Relevant (Partial Match: Core language or adjacent stack aligns)
#   1 = Marginally Relevant (Weak Match: Minor tool overlap like Git/Linux, different focus)
#   0 = Irrelevant (Zero Match: Completely different domain, e.g. Finance vs DevOps)
# ==============================================================================

PAIRS = [
    # --- GRADE 3: HIGHLY RELEVANT (5 PAIRS) ---
    {
        "id": "PAIR-01",
        "human_grade": 3,
        "resume": "Alex Rivera - Senior Python Engineer. 6 years experience with Python, FastAPI, Django, PostgreSQL, Docker, Redis, and REST APIs. Microservice architecture and automated CI/CD pipelines.",
        "jd": "Senior Python Developer: Seeking seasoned engineer proficient in Python, FastAPI, PostgreSQL, Docker, Redis, and RESTful microservices."
    },
    {
        "id": "PAIR-02",
        "human_grade": 3,
        "resume": "Samantha Wu - Lead Frontend Architect. Expertise in React.js, TypeScript, Next.js, Redux, Tailwind CSS, Jest, and Webpack. Built scalable design systems.",
        "jd": "Senior Frontend Engineer: Must have extensive React.js, TypeScript, Next.js, Tailwind CSS, Redux, and modern frontend testing experience."
    },
    {
        "id": "PAIR-03",
        "human_grade": 3,
        "resume": "Marcus Chen - Cloud DevOps Lead. 7 years managing AWS, Kubernetes, Terraform, Docker, Helm, Linux, Prometheus, Grafana, and CI/CD with GitHub Actions.",
        "jd": "DevOps Architect: Looking for containerization and cloud expert with Kubernetes, Docker, Terraform, AWS, Helm, CI/CD, and Prometheus monitoring."
    },
    {
        "id": "PAIR-04",
        "human_grade": 3,
        "resume": "Dr. Sarah Lin - Senior Machine Learning Scientist. PyTorch, TensorFlow, Scikit-Learn, Deep Learning, NLP, Computer Vision, Pandas, NumPy, Python, and MLOps on AWS.",
        "jd": "Machine Learning Engineer: Require deep knowledge of PyTorch, TensorFlow, NLP, Computer Vision, Scikit-Learn, Python, and cloud ML deployment."
    },
    {
        "id": "PAIR-05",
        "human_grade": 3,
        "resume": "David Miller - Staff Backend Engineer. Go, Golang, gRPC, PostgreSQL, Kafka, Kubernetes, Docker, Microservices, Redis, and distributed systems architecture.",
        "jd": "Staff Go Engineer: Seeking high-throughput distributed systems expert in Go, gRPC, PostgreSQL, Docker, Kubernetes, and event-driven architecture."
    },

    # --- GRADE 2: MODERATELY RELEVANT (5 PAIRS) ---
    {
        "id": "PAIR-06",
        "human_grade": 2,
        "resume": "Kevin Patel - Backend Developer. Python, Django, SQLite, Git, Linux. Built REST APIs and internal workflow tools. Learning Docker and cloud services.",
        "jd": "Full-Stack Engineer: Seeking engineer proficient in Python, FastAPI, React.js, TypeScript, Tailwind CSS, Docker, and PostgreSQL."
    },
    {
        "id": "PAIR-07",
        "human_grade": 2,
        "resume": "Rachel Green - Vue.js Frontend Developer. Vue, JavaScript, HTML5, CSS3, Tailwind CSS, Git. Some React exposure.",
        "jd": "Frontend Specialist: React.js, TypeScript, Next.js, Tailwind CSS, Redux, Jest, and Webpack."
    },
    {
        "id": "PAIR-08",
        "human_grade": 2,
        "resume": "Tom Bradley - SysAdmin & Cloud Admin. Linux, Bash, AWS EC2, S3, Docker, Git. Basic scripting and network administration.",
        "jd": "DevOps Engineer: Kubernetes, Helm, Terraform, Ansible, AWS, Docker, CI/CD pipelines, Prometheus, and Grafana."
    },
    {
        "id": "PAIR-09",
        "human_grade": 2,
        "resume": "Linda Gomez - Data Analyst. SQL, Python, Pandas, Matplotlib, Tableau, Excel, Data Analytics. Strong statistical background.",
        "jd": "Data Scientist / ML Engineer: Python, Scikit-Learn, PyTorch, Machine Learning, Deep Learning, NLP, SQL, and Docker."
    },
    {
        "id": "PAIR-10",
        "human_grade": 2,
        "resume": "James Wilson - Java Enterprise Developer. Java, Spring Boot, MySQL, REST APIs, Git. Familiar with enterprise MVC architectures.",
        "jd": "Full-Stack Java & React Developer: Java, Spring Boot, React.js, TypeScript, Docker, AWS, PostgreSQL, and Microservices."
    },

    # --- GRADE 1: MARGINALLY RELEVANT (5 PAIRS) ---
    {
        "id": "PAIR-11",
        "human_grade": 1,
        "resume": "Anna Becker - Quality Assurance Specialist. Manual testing, Jira, TestRail, Bug tracking, Agile, Scrum, Git, Basic SQL queries.",
        "jd": "Senior SDET / Automation Engineer: Must write automation frameworks in Python, PyTest, Selenium, Playwright, CI/CD, and Docker."
    },
    {
        "id": "PAIR-12",
        "human_grade": 1,
        "resume": "Brian O'Connor - Embedded C Developer. C, Assembly, Microcontrollers, RTOS, Hardware debugging, Git.",
        "jd": "Cloud Backend Engineer: Python, FastAPI, AWS, Docker, Kubernetes, GraphQL, and Redis."
    },
    {
        "id": "PAIR-13",
        "human_grade": 1,
        "resume": "Jessica Taylor - UI/UX Designer. Figma, Adobe XD, Wireframing, User Research, Prototyping, Design Systems, Basic HTML and CSS.",
        "jd": "Senior React Frontend Developer: React.js, TypeScript, Next.js, Redux, Tailwind CSS, Webpack, Unit Testing."
    },
    {
        "id": "PAIR-14",
        "human_grade": 1,
        "resume": "Carlos Mendoza - IT Helpdesk Support. Windows Server, Active Directory, Network Troubleshooting, Hardware Maintenance, Jira, Customer Service.",
        "jd": "Site Reliability Engineer (SRE): Linux, Kubernetes, Terraform, Python, Go, Docker, AWS, Prometheus, Incident Response."
    },
    {
        "id": "PAIR-15",
        "human_grade": 1,
        "resume": "Sophie Laurent - Marketing Data Specialist. Google Analytics, Excel, SEO, Content Management, Social Media, Basic SQL reporting.",
        "jd": "Big Data Engineer: Apache Spark, Hadoop, Python, Scala, Kafka, AWS, Snowflake, and Data Pipelines."
    },

    # --- GRADE 0: IRRELEVANT (5 PAIRS) ---
    {
        "id": "PAIR-16",
        "human_grade": 0,
        "resume": "Edward Norton - Senior Accountant & Financial Auditor. GAAP, Accounts Payable, Ledger reconciliation, Tax Compliance, Auditing, Corporate budgeting, Excel.",
        "jd": "Cloud Infrastructure Engineer: Kubernetes, Docker, Terraform, AWS, Linux, CI/CD, and Helm."
    },
    {
        "id": "PAIR-17",
        "human_grade": 0,
        "resume": "Victoria Sterling - Corporate Attorney & Legal Counsel. Contract Negotiation, Compliance, Intellectual Property, Employment Law, Regulatory Affairs, M&A.",
        "jd": "Full-Stack Web Developer: Python, FastAPI, React.js, TypeScript, PostgreSQL, and Tailwind CSS."
    },
    {
        "id": "PAIR-18",
        "human_grade": 0,
        "resume": "Chef Antonio Rossi - Executive Chef & Restaurant Manager. Menu planning, Culinary arts, Food safety, Staff leadership, Inventory control, Kitchen budgeting.",
        "jd": "Senior Machine Learning Engineer: PyTorch, TensorFlow, Deep Learning, Computer Vision, Python, and CUDA."
    },
    {
        "id": "PAIR-19",
        "human_grade": 0,
        "resume": "Hannah Abbott - Registered Nurse & Clinical Coordinator. Patient triage, Electronic health records, Emergency care, Medication administration, Patient advocacy.",
        "jd": "Golang Backend Developer: Go, Microservices, gRPC, Docker, Kubernetes, PostgreSQL, and Redis."
    },
    {
        "id": "PAIR-20",
        "human_grade": 0,
        "resume": "Robert Langdon - Museum Curator & Art Historian. Archival preservation, Gallery exhibitions, Art restoration, Public lecturing, Cataloging antiquities.",
        "jd": "Cybersecurity Penetration Tester: Kali Linux, Metasploit, Wireshark, Python, Network Security, CEH, Vulnerability Assessment."
    }
]

def dcg_at_k(r, k):
    r = np.asfarray(r)[:k]
    if r.size:
        return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
    return 0.0

def ndcg_at_k(r, k):
    dcg_max = dcg_at_k(sorted(r, reverse=True), k)
    if not dcg_max:
        return 0.0
    return dcg_at_k(r, k) / dcg_max

def evaluate_ranking():
    print("=" * 85)
    print("      INDEPENDENT MATCHING QUALITY & RANKING EVALUATION (20 RESUME-JD PAIRS)")
    print("=" * 85)
    
    evaluated = []
    
    for p in PAIRS:
        sim_res = calculate_similarity_score(p["resume"], p["jd"])
        skill_res = compare_skills(p["resume"], p["jd"])
        
        score = sim_res["match_score"]
        coverage = skill_res["skill_coverage_percentage"]
        matched_skills = skill_res["matching_skills"]
        missing_skills = skill_res["missing_skills"]
        
        evaluated.append({
            "id": p["id"],
            "human_grade": p["human_grade"],
            "score": score,
            "coverage": coverage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })
        
    # Sort by algorithm match score descending
    ranked_by_score = sorted(evaluated, key=lambda x: x["score"], reverse=True)
    
    print(f"{'Rank':<5} | {'Pair ID':<8} | {'Human Grade':<12} | {'Score %':<8} | {'Coverage %':<11} | {'Matched Skills'}")
    print("-" * 85)
    
    relevance_scores_ranked = []
    for rank, item in enumerate(ranked_by_score, 1):
        relevance_scores_ranked.append(item["human_grade"])
        matched_str = ", ".join(item["matched_skills"][:4])
        print(f"{rank:<5} | {item['id']:<8} | Grade {item['human_grade']:<6} | {item['score']:<8.1f} | {item['coverage']:<11.1f} | {matched_str}")
        
    # Calculate IR Metrics
    # Relevant items defined as Grade >= 2 (Moderately or Highly relevant)
    k_values = [5, 10, 20]
    
    print("\n" + "=" * 85)
    print("                         INFORMATION RETRIEVAL RANKING METRICS         ")
    print("=" * 85)
    
    ndcg_5 = ndcg_at_k(relevance_scores_ranked, 5)
    ndcg_10 = ndcg_at_k(relevance_scores_ranked, 10)
    ndcg_20 = ndcg_at_k(relevance_scores_ranked, 20)
    
    # Precision@K: fraction of top K that are relevant (human_grade >= 2)
    p_at_5 = sum(1 for g in relevance_scores_ranked[:5] if g >= 2) / 5.0
    p_at_10 = sum(1 for g in relevance_scores_ranked[:10] if g >= 2) / 10.0
    
    # Spearman rank correlation
    from scipy.stats import spearmanr
    algo_scores = [item["score"] for item in evaluated]
    human_grades = [item["human_grade"] for item in evaluated]
    rho, p_val = spearmanr(algo_scores, human_grades)
    
    # Average score per human grade bracket
    grade_averages = {}
    for g in [3, 2, 1, 0]:
        scores = [item["score"] for item in evaluated if item["human_grade"] == g]
        grade_averages[g] = np.mean(scores) if scores else 0.0
        
    print(f"NDCG@5  : {ndcg_5:.4f} (Ideal = 1.0000)")
    print(f"NDCG@10 : {ndcg_10:.4f} (Ideal = 1.0000)")
    print(f"NDCG@20 : {ndcg_20:.4f} (Ideal = 1.0000)")
    print(f"Precision@5  (Relevant >= Grade 2): {p_at_5*100:.1f}%")
    print(f"Precision@10 (Relevant >= Grade 2): {p_at_10*100:.1f}%")
    print(f"Spearman's Rank Correlation (rho): {rho:.4f} (p-value: {p_val:.2e})")
    
    print("\nScore Separation Across Human Ground-Truth Brackets:")
    print(f"  • Grade 3 (Highly Relevant)   Mean Score: {grade_averages[3]:.1f}%")
    print(f"  • Grade 2 (Moderately Relevant) Mean Score: {grade_averages[2]:.1f}%")
    print(f"  • Grade 1 (Marginally Relevant) Mean Score: {grade_averages[1]:.1f}%")
    print(f"  • Grade 0 (Irrelevant / Poor) Mean Score: {grade_averages[0]:.1f}%")
    print("=" * 85)
    
    import json
    with open("backend/matching_quality_ranking_results.json", "w") as f:
        json.dump({
            "metrics": {
                "ndcg_at_5": round(ndcg_5, 4),
                "ndcg_at_10": round(ndcg_10, 4),
                "ndcg_at_20": round(ndcg_20, 4),
                "precision_at_5": round(p_at_5 * 100, 1),
                "precision_at_10": round(p_at_10 * 100, 1),
                "spearman_rho": round(rho, 4),
                "spearman_p_val": float(p_val)
            },
            "grade_means": {
                "grade_3": round(grade_averages[3], 1),
                "grade_2": round(grade_averages[2], 1),
                "grade_1": round(grade_averages[1], 1),
                "grade_0": round(grade_averages[0], 1)
            },
            "ranked_pairs": ranked_by_score
        }, f, indent=2)

if __name__ == "__main__":
    evaluate_ranking()
