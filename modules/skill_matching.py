"""Skill matching module to compare candidate skills with job requirements."""

import re

# ---------------------------------------------------------
# Predefined Technical Skills Catalog
# ---------------------------------------------------------
# Common technical skills used to filter and identify actual tech requirements
# from general natural language keywords in job descriptions.
PREDEFINED_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Flask",
    "Django",
    "React",
    "Node.js",
    "Streamlit"
]


class SkillMatchResult(tuple):
    """Container for skill match results.

    Supports both tuple unpacking:
        matched, missing, percentage = match_skills(...)
    and dictionary/property access:
        result.matched_skills or result["matched_skills"]
    """

    def __new__(cls, matched_skills, missing_skills, match_percentage, job_skills=None):
        return super().__new__(cls, (matched_skills, missing_skills, match_percentage))

    def __init__(self, matched_skills, missing_skills, match_percentage, job_skills=None):
        self.matched_skills = matched_skills
        self.missing_skills = missing_skills
        self.match_percentage = match_percentage
        self.job_skills = job_skills if job_skills is not None else (matched_skills + missing_skills)

    def __getitem__(self, key):
        if isinstance(key, str):
            if key == "matched_skills":
                return self.matched_skills
            elif key == "missing_skills":
                return self.missing_skills
            elif key == "match_percentage":
                return self.match_percentage
            elif key == "job_skills":
                return self.job_skills
            raise KeyError(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


def extract_technical_skills(text_or_keywords) -> list:
    """Identify and extract technical skills from text or keyword lists.

    Supports:
    - Single-word skills (e.g., Python, SQL, Docker)
    - Multi-word skills (e.g., Machine Learning, Data Science, Deep Learning)
    - Special syntax skills (e.g., C++, Node.js)
    """
    if not text_or_keywords:
        return []

    # If a list of words/tokens is passed, join them into a searchable string
    if isinstance(text_or_keywords, (list, set, tuple)):
        search_text = " " + " ".join(str(w) for w in text_or_keywords) + " "
    elif isinstance(text_or_keywords, str):
        search_text = " " + text_or_keywords + " "
    else:
        return []

    search_text_lower = search_text.lower()
    detected_skills = []

    for skill in PREDEFINED_SKILLS:
        skill_lower = skill.lower()

        # Handle regex pattern matching for distinct skills
        if skill_lower == "c++":
            # Match c++ preceded and followed by non-word/boundary chars
            pattern = r"(?:\b|\s)c\+\+(?:[\s,.;:!?]|$)"
        elif skill_lower == "c":
            # Match standalone C letter without matching 'c' inside words
            pattern = r"(?:\b|\s)c(?:[\s,.;:!?]|$)"
        elif skill_lower == "node.js":
            # Match Node.js or NodeJS or Node js
            pattern = r"\bnode(?:\.js|\s*js)?\b"
        elif skill_lower == "react":
            # Match React or React.js
            pattern = r"\breact(?:\.js|\s*js)?\b"
        else:
            # Word boundary matching for standard skills & multi-word phrases
            escaped = re.escape(skill_lower)
            pattern = rf"\b{escaped}\b"

        if re.search(pattern, search_text_lower):
            detected_skills.append(skill)

    return detected_skills


def normalize_candidate_skills(candidate_skills) -> set:
    """Normalize candidate skills by converting to lowercase and stripping extra spaces.

    Accepts comma-separated strings or lists of skills.
    """
    if not candidate_skills:
        return set()

    if isinstance(candidate_skills, str):
        # Split on commas or newlines
        raw_items = re.split(r"[,;\n]+", candidate_skills)
    elif isinstance(candidate_skills, (list, set, tuple)):
        raw_items = candidate_skills
    else:
        raw_items = [str(candidate_skills)]

    normalized = set()
    for item in raw_items:
        cleaned = item.strip().lower()
        if cleaned:
            normalized.add(cleaned)
            # Also normalize variations like node.js / nodejs
            if cleaned in ("node.js", "nodejs", "node js"):
                normalized.add("node.js")
            if cleaned in ("react.js", "reactjs", "react js"):
                normalized.add("react")

    return normalized


def match_skills(candidate_skills, job_keywords) -> SkillMatchResult:
    """Compare candidate skills against job requirements.

    Steps:
    1. Normalize candidate skills (lowercase, whitespace trimmed, comma-separated split).
    2. Normalize and identify relevant technical skills from job requirements.
    3. Categorize into matched_skills and missing_skills.
    4. Compute match_percentage = (matched / total job skills) * 100.
    """
    # 1. Normalize candidate skills into a clean lowercase set
    candidate_norm = normalize_candidate_skills(candidate_skills)

    # 2. Identify relevant technical skills from the job keywords or text
    # Checks against PREDEFINED_SKILLS so general words are not treated as tech skills
    relevant_job_skills = extract_technical_skills(job_keywords)

    matched_skills = []
    missing_skills = []

    # 3. Compare each relevant job skill against candidate skills
    for job_skill in relevant_job_skills:
        job_skill_lower = job_skill.lower()

        # Check direct or normalized match
        is_matched = False
        if job_skill_lower in candidate_norm:
            is_matched = True
        else:
            # Check if any candidate skill matches canonical name
            for cand_skill in candidate_norm:
                if cand_skill == job_skill_lower:
                    is_matched = True
                    break

        if is_matched:
            matched_skills.append(job_skill)
        else:
            missing_skills.append(job_skill)

    # 4. Calculate match percentage avoiding division by zero
    total_relevant = len(relevant_job_skills)
    if total_relevant > 0:
        match_percentage = round((len(matched_skills) / total_relevant) * 100)
    else:
        match_percentage = 0

    return SkillMatchResult(matched_skills, missing_skills, match_percentage, relevant_job_skills)
