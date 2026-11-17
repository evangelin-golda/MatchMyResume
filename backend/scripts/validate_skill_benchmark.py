import re
from typing import Set, Dict, List
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
for p in [BACKEND_DIR, PROJECT_ROOT]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.services.skill_service import extract_skills
except ImportError:
    from backend.app.services.skill_service import extract_skills

# ==============================================================================
# EXPANDED SKILL EXTRACTION BENCHMARK (100+ Ground-Truth Skill Instances)
# Dataset Nature: Curated Realistic Synthetic Resumes and Job Descriptions
# Annotated manually according to documented industry engineering skill taxonomy
# ==============================================================================

BENCHMARK_CASES = [
    {
        "id": "BENCH-01",
        "category": "Core Full-Stack & Plurals",
        "description": "Standard full stack profile with plural frameworks and compound terms",
        "text": """
        Elena Rostova - Full Stack Architect
        Summary: 8+ years architecting web platforms utilizing Python, FastAPI, React.js, and TypeScript.
        Core Competencies: PostgreSQL, Redis, Docker, Git, REST APIs, Microservices, Tailwind CSS.
        Professional Skills: Problem Solving, Collaboration, Team Leadership, Agile Methodologies.
        """,
        "ground_truth": {
            "Python", "FastAPI", "React.js", "TypeScript", "PostgreSQL", "Redis",
            "Docker", "Git", "REST APIs", "Microservices", "Tailwind CSS",
            "Problem Solving", "Collaboration", "Team Leadership", "Agile Methodologies"
        }
    },
    {
        "id": "BENCH-02",
        "category": "Data Science & Machine Learning",
        "description": "Data scientist profile with abbreviations and compound AI terms",
        "text": """
        Dr. Marcus Vance - Principal AI Researcher
        Technical Background: Machine Learning, Deep Learning, Natural Language Processing, Computer Vision.
        Libraries & Tooling: PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, Keras, Matplotlib, Seaborn.
        Infrastructure & Data: Python, R, SQL, Spark, Hadoop, AWS, Docker.
        Soft Skills: Analytical Thinking, Critical Thinking, Mentorship, Presentation Skills.
        """,
        "ground_truth": {
            "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision",
            "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "Keras", "Matplotlib", "Seaborn",
            "Python", "R", "SQL", "Spark", "Hadoop", "AWS", "Docker",
            "Analytical Thinking", "Critical Thinking", "Mentorship", "Presentation Skills"
        }
    },
    {
        "id": "BENCH-03",
        "category": "DevOps & Cloud Engineering",
        "description": "DevOps profile with cloud tools, orchestrators, and CI/CD pipelines",
        "text": """
        DevOps & Platform Specialist:
        Cloud Platforms: AWS, Azure, Google Cloud.
        Containerization & Orchestration: Docker, Kubernetes, Helm.
        Infrastructure as Code & CI/CD: Terraform, Ansible, CI/CD, GitHub Actions, GitLab CI, Jenkins.
        Monitoring & Systems: Linux, Bash, Prometheus, Grafana, Nginx.
        Execution: Cross-Functional Collaboration, Time Management, Continuous Learning.
        """,
        "ground_truth": {
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Helm",
            "Terraform", "Ansible", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins",
            "Linux", "Bash", "Prometheus", "Grafana", "Nginx",
            "Cross-Functional Collaboration", "Time Management", "Continuous Learning"
        }
    },
    {
        "id": "BENCH-04",
        "category": "Similar But Distinct Languages (Disambiguation)",
        "description": "Tests boundary isolation for Java vs JavaScript, C vs C++ vs C#, and Go",
        "text": """
        Polyglot Systems Engineer:
        Proficient in Java enterprise services and modern JavaScript frontend applications.
        Low-level embedded development in C++ and C# desktop platforms.
        Backend microservices built with Go (Golang) and Rust.
        Scripts written in Shell and PowerShell.
        Communication skills and Attention to Detail.
        """,
        "ground_truth": {
            "Java", "JavaScript", "C++", "C#", "Go", "Rust", "Shell", "PowerShell",
            "Communication", "Attention to Detail"
        }
    },
    {
        "id": "BENCH-05",
        "category": "Compound Skills & Sub-token Containment",
        "description": "Verifies that compound skills do not produce false positive sub-matches unless standalone",
        "text": """
        UI/UX Developer:
        Built responsive applications with Tailwind CSS and Next.js.
        Also possesses standalone expertise in CSS, HTML, and Sass.
        Utilizes Webpack and Vite for bundling.
        Employs Jest and Cypress for unit testing and end-to-end verification.
        Demonstrates Adaptability and Work Ethic.
        """,
        "ground_truth": {
            "Tailwind CSS", "Next.js", "CSS", "HTML", "Sass", "Webpack", "Vite",
            "Jest", "Cypress", "Unit Testing", "Adaptability", "Work Ethic"
        }
    },
    {
        "id": "BENCH-06",
        "category": "False Positive Resistance (Unrelated English Contexts)",
        "description": "Tests words that resemble skill names in everyday prose (e.g. 'go', 'catered', 'swift')",
        "text": """
        Operations Manager Profile:
        Led a team to go to international conferences and negotiated client contracts.
        Ensured swift resolution of shipping escalations and catered to high-value stakeholders.
        Used Microsoft Excel and Jira for tracking.
        Strong Decision Making, Conflict Resolution, and Negotiation abilities.
        """,
        "ground_truth": {
            # "go" should NOT match English verb "to go"
            # "catered" should NOT match "C"
            # "swift" in "swift resolution" should ideally not match Swift (or if it does, count as FP)
            # Legitimate skills in taxonomy:
            "Jira", "Decision Making", "Conflict Resolution", "Negotiation"
        }
    },
    {
        "id": "BENCH-07",
        "category": "Repeated Skills & Case Invariance",
        "description": "Tests duplicate mentions across sections and mixed capitalization",
        "text": """
        PYTHON DEVELOPER - PYTHON BACKEND SPECIALIST
        Summary: Python enthusiast building python tools.
        Skills: python, PYTHON, PyThOn, Django, PostgreSQL, Docker, Git.
        Experience: Developed Python REST APIs using Django and Docker.
        Soft Skills: Teamwork, teamwork, TEAMWORK.
        """,
        "ground_truth": {
            "Python", "Django", "PostgreSQL", "Docker", "Git", "REST APIs", "Teamwork"
        }
    },
    {
        "id": "BENCH-08",
        "category": "Unusual Resume Sections & Side Projects",
        "description": "Skills buried in hackathons, open source, and personal interests",
        "text": """
        Candidate Profile - Non-Traditional Format
        [Weekend Hacking & Open Source]
        Built a Telegram bot using Flask and SQLite.
        Experimented with LLM fine-tuning using Hugging Face and LangChain.
        Stored embeddings in ChromaDB and Pinecone.
        [Extracurricular Activities]
        Organized community Hackathon; demonstrated Project Management and Creativity.
        """,
        "ground_truth": {
            "Flask", "SQLite", "LLM", "Hugging Face", "LangChain", "ChromaDB", "Pinecone",
            "Project Management", "Creativity"
        }
    },
    {
        "id": "BENCH-09",
        "category": "Modern Frontend & State Management",
        "description": "Contemporary frontend stack with state stores and UI libraries",
        "text": """
        Senior Frontend Engineer:
        Core: Vue.js, Vue, Angular, Svelte, Redux, Zustand.
        Styles & Frameworks: Bootstrap, Material-UI, Chakra-UI, HTML5, CSS3.
        Testing: Playwright, TDD, Unit Testing.
        Agile Methodologies: Scrum, Kanban, Agile Mindset.
        """,
        "ground_truth": {
            "Vue.js", "Angular", "Svelte", "Redux", "Zustand",
            "Bootstrap", "Material-UI", "Chakra-UI", "HTML5", "CSS3",
            "Playwright", "TDD", "Unit Testing", "Scrum", "Kanban", "Agile Mindset"
        }
    },
    {
        "id": "BENCH-10",
        "category": "Enterprise Backend & Databases",
        "description": "Enterprise server architecture and multi-model databases",
        "text": """
        Enterprise Systems Architect:
        Backend Frameworks: Spring Boot, ASP.NET, Express.js, Nest.js, Node.js, GraphQL, gRPC.
        Databases: MySQL, MongoDB, Cassandra, DynamoDB, Firebase, Supabase, MariaDB, Neo4j, Oracle, Snowflake.
        Leadership: Stakeholder Management, Client Communication, Written Communication, Verbal Communication.
        """,
        "ground_truth": {
            "Spring Boot", "ASP.NET", "Express.js", "Nest.js", "Node.js", "GraphQL", "gRPC",
            "MySQL", "MongoDB", "Cassandra", "DynamoDB", "Firebase", "Supabase", "MariaDB", "Neo4j", "Oracle", "Snowflake",
            "Stakeholder Management", "Client Communication", "Written Communication", "Verbal Communication"
        }
    }
]

def run_benchmark():
    total_gt = 0
    total_tp = 0
    total_fp = 0
    total_fn = 0
    
    print("=" * 80)
    print("   EXPANDED SKILL EXTRACTION BENCHMARK EVALUATION (10 TEST CASES, 100+ SKILLS)")
    print("=" * 80)
    
    case_summaries = []
    
    for case in BENCHMARK_CASES:
        gt = case["ground_truth"]
        total_gt += len(gt)
        
        tech, soft = extract_skills(case["text"])
        predicted = tech.union(soft)
        
        tp_set = predicted.intersection(gt)
        fp_set = predicted.difference(gt)
        fn_set = gt.difference(predicted)
        
        tp = len(tp_set)
        fp = len(fp_set)
        fn = len(fn_set)
        
        total_tp += tp
        total_fp += fp
        total_fn += fn
        
        prec = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        
        print(f"\n[{case['id']}] {case['category']}")
        print(f"  Description: {case['description']}")
        print(f"  Ground Truth ({len(gt)}): {sorted(list(gt))}")
        print(f"  Predicted    ({len(predicted)}): {sorted(list(predicted))}")
        print(f"  TP: {tp} | FP: {fp} ({sorted(list(fp_set))}) | FN: {fn} ({sorted(list(fn_set))})")
        print(f"  Precision: {prec*100:.1f}% | Recall: {rec*100:.1f}% | F1: {f1*100:.1f}%")
        
        case_summaries.append({
            "id": case["id"],
            "category": case["category"],
            "gt_count": len(gt),
            "predicted_count": len(predicted),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "fp_list": sorted(list(fp_set)),
            "fn_list": sorted(list(fn_set)),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1": round(f1 * 100, 2)
        })
        
    overall_prec = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_rec = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = (2 * overall_prec * overall_rec) / (overall_prec + overall_rec) if (overall_prec + overall_rec) > 0 else 0.0
    
    print("\n" + "=" * 80)
    print("                    OVERALL BENCHMARK PERFORMANCE                      ")
    print("=" * 80)
    print(f"Total Ground-Truth Skill Instances Tested: {total_gt}")
    print(f"Total True Positives  (TP): {total_tp}")
    print(f"Total False Positives (FP): {total_fp}")
    print(f"Total False Negatives (FN): {total_fn}")
    print(f"Micro-Average Precision   : {overall_prec*100:.2f}%")
    print(f"Micro-Average Recall      : {overall_rec*100:.2f}%")
    print(f"Micro-Average F1-Score    : {overall_f1*100:.2f}%")
    print("=" * 80)
    
    import json
    reports_dir = os.path.join(PROJECT_ROOT, "docs", "test-reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, "expanded_skill_benchmark_results.json")
    with open(report_file, "w") as f:
        json.dump({
            "total_ground_truth": total_gt,
            "total_tp": total_tp,
            "total_fp": total_fp,
            "total_fn": total_fn,
            "precision": round(overall_prec * 100, 2),
            "recall": round(overall_rec * 100, 2),
            "f1": round(overall_f1 * 100, 2),
            "cases": case_summaries
        }, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
