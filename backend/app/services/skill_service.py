import re
from typing import Dict, List, Set, Tuple

# Curated Technical Skills
TECHNICAL_SKILLS = {
    # Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "sql", "html", "css", "bash",
    "shell", "powershell",
    
    # Frontend Frameworks & Libraries
    "react", "react.js", "next.js", "vue", "vue.js", "angular", "svelte", "redux", "zustand",
    "tailwind css", "bootstrap", "sass", "material-ui", "chakra-ui", "html5", "css3", "webpack", "vite",
    
    # Backend Frameworks
    "fastapi", "django", "flask", "node.js", "express.js", "nest.js", "spring boot", "asp.net",
    "ruby on rails", "gin", "fiber", "laravel", "graphql", "rest api", "rest apis", "restful api", "restful apis", "grpc",
    "websockets", "microservices",
    
    # Databases & Caching
    "postgresql", "postgres", "mysql", "mongodb", "sqlite", "redis", "elasticsearch", "cassandra",
    "dynamodb", "firebase", "supabase", "mariadb", "neo4j", "oracle", "snowflake",
    
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "ci/cd", "github actions", "gitlab ci", "jenkins", "helm", "linux",
    "nginx", "serverless", "cloudformation", "prometheus", "grafana",
    
    # AI / ML / Data Science
    "machine learning", "deep learning", "nlp", "natural language processing", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",
    "llm", "large language models", "gemini", "openai", "langchain", "hugging face", "vector database",
    "faiss", "pinecone", "chromadb", "data analytics", "data engineering", "spark", "hadoop",
    
    # Tools & Methodologies
    "git", "github", "gitlab", "jira", "postman", "figma", "agile", "scrum", "kanban", "tdd",
    "unit testing", "pytest", "jest", "cypress", "playwright"
}

# Curated Soft & Professional Skills
SOFT_SKILLS = {
    "problem solving", "analytical thinking", "critical thinking", "communication",
    "written communication", "verbal communication", "teamwork", "collaboration",
    "cross-functional collaboration", "leadership", "team leadership", "mentorship",
    "project management", "time management", "adaptability", "flexibility",
    "stakeholder management", "decision making", "presentation skills", "work ethic",
    "attention to detail", "creativity", "conflict resolution", "negotiation",
    "agile mindset", "continuous learning", "client communication"
}

# Skill canonical name mappings (for pretty display)
CANONICAL_NAMES = {
    "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript",
    "java": "Java", "c++": "C++", "c#": "C#", "go": "Go", "golang": "Go", "rust": "Rust",
    "react": "React.js", "react.js": "React.js", "next.js": "Next.js", "vue": "Vue.js",
    "fastapi": "FastAPI", "django": "Django", "flask": "Flask", "node.js": "Node.js",
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "mongodb": "MongoDB", "redis": "Redis",
    "aws": "AWS", "gcp": "Google Cloud", "azure": "Azure", "docker": "Docker",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes", "git": "Git", "sql": "SQL",
    "tailwind css": "Tailwind CSS", "rest api": "REST APIs", "rest apis": "REST APIs",
    "restful api": "REST APIs", "restful apis": "REST APIs",
    "html": "HTML", "html5": "HTML5", "css": "CSS", "css3": "CSS3",
    # Cloud & DevOps
    "ci/cd": "CI/CD", "github actions": "GitHub Actions", "gitlab ci": "GitLab CI", "graphql": "GraphQL",
    "gcp": "Google Cloud", "google cloud": "Google Cloud", "azure": "Azure", "helm": "Helm",
    "prometheus": "Prometheus", "grafana": "Grafana", "nginx": "Nginx", "linux": "Linux",
    "powershell": "PowerShell", "shell": "Shell", "bash": "Bash",
    
    # Frameworks & UI
    "next.js": "Next.js", "vue": "Vue.js", "vue.js": "Vue.js", "express.js": "Express.js",
    "nest.js": "Nest.js", "spring boot": "Spring Boot", "asp.net": "ASP.NET",
    "material-ui": "Material-UI", "chakra-ui": "Chakra-UI", "bootstrap": "Bootstrap",
    "sass": "Sass", "webpack": "Webpack", "vite": "Vite", "redux": "Redux", "zustand": "Zustand",
    
    # Testing
    "tdd": "TDD", "unit testing": "Unit Testing", "jest": "Jest", "cypress": "Cypress",
    "playwright": "Playwright", "pytest": "PyTest",
    
    # Databases & Big Data
    "mysql": "MySQL", "sqlite": "SQLite", "dynamodb": "DynamoDB", "mariadb": "MariaDB",
    "neo4j": "Neo4j", "cassandra": "Cassandra", "oracle": "Oracle", "snowflake": "Snowflake",
    "firebase": "Firebase", "supabase": "Supabase", "spark": "Spark", "hadoop": "Hadoop",
    "chromadb": "ChromaDB", "pinecone": "Pinecone", "faiss": "FAISS",
    
    # AI / ML
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "nlp": "Natural Language Processing", "scikit-learn": "Scikit-Learn", "pytorch": "PyTorch",
    "tensorflow": "TensorFlow", "pandas": "Pandas", "numpy": "NumPy", "keras": "Keras",
    "matplotlib": "Matplotlib", "seaborn": "Seaborn", "llm": "LLM", "large language models": "LLM",
    "langchain": "LangChain", "hugging face": "Hugging Face", "grpc": "gRPC",
    
    # Soft & Professional
    "problem solving": "Problem Solving", "collaboration": "Collaboration",
    "cross-functional collaboration": "Cross-Functional Collaboration",
    "leadership": "Leadership", "team leadership": "Team Leadership", "mentorship": "Mentorship",
    "agile": "Agile Methodologies", "scrum": "Scrum", "kanban": "Kanban",
    "agile mindset": "Agile Mindset", "communication": "Communication",
    "attention to detail": "Attention to Detail", "analytical thinking": "Analytical Thinking",
    "critical thinking": "Critical Thinking", "presentation skills": "Presentation Skills",
    "time management": "Time Management", "continuous learning": "Continuous Learning",
    "adaptability": "Adaptability", "work ethic": "Work Ethic", "decision making": "Decision Making",
    "conflict resolution": "Conflict Resolution", "negotiation": "Negotiation",
    "project management": "Project Management", "creativity": "Creativity",
    "stakeholder management": "Stakeholder Management", "client communication": "Client Communication",
    "written communication": "Written Communication", "verbal communication": "Verbal Communication"
}

def clean_and_tokenize(text: str) -> str:
    """Preprocess text for normalized matching."""
    text = text.lower()
    text = re.sub(r'[\r\n\t]+', ' ', text)
    return text

def extract_skills(text: str) -> Tuple[Set[str], Set[str]]:
    """
    Extracts technical and soft skills from given text using boundary-safe regex
    with phrase-span masking to avoid spurious sub-token matches.
    Returns (technical_skills, soft_skills) with canonical casing.
    """
    cleaned = clean_and_tokenize(text)
    
    # Sort all skills by length descending to prioritize longer multi-word phrases
    all_skills = sorted(list(TECHNICAL_SKILLS.union(SOFT_SKILLS)), key=lambda s: len(s), reverse=True)
    
    matched_spans = []
    found_tech = set()
    found_soft = set()
    
    for skill in all_skills:
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
        matches = list(re.finditer(pattern, cleaned))
        if not matches:
            continue
            
        # Keep skill if at least one match is not purely a sub-span of an already matched longer phrase
        independent_matches = []
        for m in matches:
            m_start, m_end = m.span()
            is_subspan = any(span_start <= m_start and m_end <= span_end for span_start, span_end in matched_spans)
            if not is_subspan:
                independent_matches.append((m_start, m_end))
                
        if independent_matches:
            matched_spans.extend(independent_matches)
            canonical = CANONICAL_NAMES.get(skill, skill.title())
            if skill in TECHNICAL_SKILLS:
                found_tech.add(canonical)
            if skill in SOFT_SKILLS:
                found_soft.add(canonical)
                
    return found_tech, found_soft

def compare_skills(resume_text: str, job_description: str) -> Dict:
    """
    Compares skills found in the resume against skills found in the job description.
    """
    res_tech, res_soft = extract_skills(resume_text)
    jd_tech, jd_soft = extract_skills(job_description)
    
    all_res_skills = res_tech.union(res_soft)
    all_jd_skills = jd_tech.union(jd_soft)
    
    matching_tech = sorted(list(res_tech.intersection(jd_tech)))
    missing_tech = sorted(list(jd_tech.difference(res_tech)))
    additional_tech = sorted(list(res_tech.difference(jd_tech)))
    
    matching_soft = sorted(list(res_soft.intersection(jd_soft)))
    missing_soft = sorted(list(jd_soft.difference(res_soft)))
    additional_soft = sorted(list(res_soft.difference(jd_soft)))
    
    matching_all = sorted(list(all_res_skills.intersection(all_jd_skills)))
    missing_all = sorted(list(all_jd_skills.difference(all_res_skills)))
    additional_all = sorted(list(all_res_skills.difference(all_jd_skills)))
    
    # Calculate skill coverage ratio
    total_required = len(all_jd_skills)
    matched_count = len(matching_all)
    skill_coverage = round((matched_count / total_required * 100), 1) if total_required > 0 else 100.0
    
    return {
        "matching_skills": matching_all,
        "missing_skills": missing_all,
        "additional_skills": additional_all,
        "matching_technical": matching_tech,
        "missing_technical": missing_tech,
        "additional_technical": additional_tech,
        "matching_soft": matching_soft,
        "missing_soft": missing_soft,
        "additional_soft": additional_soft,
        "skill_coverage_percentage": skill_coverage,
        "total_required_skills": total_required,
        "total_matched_skills": matched_count
    }
