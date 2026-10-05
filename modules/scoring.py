"""Scoring module to calculate cover letter quality and relevance score."""

import re

# ---------------------------------------------------------
# Professional Vocabulary Catalog
# ---------------------------------------------------------
PROFESSIONAL_KEYWORDS = [
    "experience",
    "skills",
    "contribute",
    "opportunity",
    "qualifications",
    "professional",
    "interested",
    "application",
    "position",
    "organization"
]


class QualityScoreResult(tuple):
    """Container for cover letter quality score results.

    Supports both tuple unpacking:
        total, wc, kw, struct, prof, pers, fb = calculate_score(...)
    and attribute / dictionary key access:
        result.total_score, result["total_score"]
    """

    def __new__(cls, total_score, word_count_score, keyword_score,
                structure_score, professionalism_score, personalization_score,
                feedback, word_count=0):
        return super().__new__(
            cls,
            (total_score, word_count_score, keyword_score,
             structure_score, professionalism_score, personalization_score, feedback)
        )

    def __init__(self, total_score, word_count_score, keyword_score,
                 structure_score, professionalism_score, personalization_score,
                 feedback, word_count=0):
        self.total_score = total_score
        self.word_count_score = word_count_score
        self.keyword_score = keyword_score
        self.structure_score = structure_score
        self.professionalism_score = professionalism_score
        self.personalization_score = personalization_score
        self.feedback = feedback
        self.word_count = word_count

    def __getitem__(self, key):
        if isinstance(key, str):
            mapping = {
                "total_score": self.total_score,
                "word_count_score": self.word_count_score,
                "keyword_score": self.keyword_score,
                "structure_score": self.structure_score,
                "professionalism_score": self.professionalism_score,
                "personalization_score": self.personalization_score,
                "feedback": self.feedback,
                "word_count": self.word_count
            }
            if key in mapping:
                return mapping[key]
            raise KeyError(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


def _field_in_text(field_val: str, text_lower: str) -> bool:
    """Check whether candidate information appears in the text."""
    if not field_val or not isinstance(field_val, str):
        return False
    val_clean = field_val.strip().lower()
    if not val_clean or val_clean in ("not provided", "none", "n/a"):
        return False

    # Exact full match
    if val_clean in text_lower:
        return True

    # Check for meaningful words or subphrases (length >= 4)
    words = [w for w in re.findall(r"[a-zA-Z0-9]+", val_clean) if len(w) >= 4]
    if words and any(w in text_lower for w in words):
        return True

    return False


def calculate_score(cover_letter: str, job_skills: list, candidate_profile: dict) -> QualityScoreResult:
    """Evaluate a cover letter across five quality metrics based on ACTUAL text content.

    1. Word Count Score (20 points):
       - 150–400 words = 20 points
       - 100–149 words = 15 points
       - 50–99 words = 10 points
       - 1–49 words = 5 points
       - 0 words = 0 points

    2. Keyword Match Score (30 points):
       - (matched_count / total_job_skills) * 30
       - If total_job_skills == 0, score is 0.
       - Supports multi-word skills (machine learning, data science, etc.).

    3. Structure Score (20 points):
       - 4 points each for: Greeting, Opening, Body, Closing, Sign-off/Name.

    4. Professional Language Score (20 points):
       - Count presence of 10 professional keywords (2 points each, max 20).

    5. Personalization Score (10 points):
       - Checks presence of candidate details (name, education, projects, experience, achievements).
       - Only checks fields that actually contain information.
    """
    candidate_profile = candidate_profile or {}
    job_skills = job_skills or []
    feedback = []

    if not cover_letter or not isinstance(cover_letter, str):
        cover_letter = ""

    cover_letter_clean = cover_letter.strip()
    words = cover_letter_clean.split()
    word_count = len(words)
    text_lower = cover_letter_clean.lower()

    # ---------------------------------------------------------
    # 1. WORD COUNT SCORE — 20 points
    # ---------------------------------------------------------
    if 150 <= word_count <= 400:
        word_count_score = 20
    elif 100 <= word_count <= 149:
        word_count_score = 15
    elif 50 <= word_count <= 99:
        word_count_score = 10
    elif 1 <= word_count <= 49:
        word_count_score = 5
    else:
        word_count_score = 0

    if word_count_score < 20:
        feedback.append("Consider adding more relevant details to reach a professional cover letter length.")
    else:
        feedback.append(f"Ideal cover letter length ({word_count} words).")

    # ---------------------------------------------------------
    # 2. KEYWORD MATCH SCORE — 30 points
    # ---------------------------------------------------------
    # Clean and normalize job skills
    normalized_job_skills = [
        str(skill).strip().lower()
        for skill in job_skills
        if str(skill).strip()
    ]
    # Remove duplicates while preserving order
    unique_job_skills = list(dict.fromkeys(normalized_job_skills))
    total_job_skills = len(unique_job_skills)

    if total_job_skills == 0:
        keyword_score = 0
        matched_count = 0
        feedback.append("No technical skills were provided from the job description to match against.")
    else:
        # Check presence of each skill (handles single-word and multi-word skills)
        matched_count = sum(1 for skill in unique_job_skills if skill in text_lower)
        keyword_score = round((matched_count / total_job_skills) * 30)

        if keyword_score < 20:
            feedback.append("Add more job-relevant skills and keywords.")
        else:
            feedback.append(f"Strong keyword alignment ({matched_count}/{total_job_skills} target skills mentioned).")

    # ---------------------------------------------------------
    # 3. STRUCTURE SCORE — 20 points
    # ---------------------------------------------------------
    # 1. Greeting (e.g. "Dear Hiring Manager", "Dear ...", "Hello")
    has_greeting = bool(re.search(r"\b(dear|hello|to whom|greetings|hi)\b", text_lower))

    # 2. Opening content
    has_opening = bool(re.search(r"\b(writing to|application for|apply for|excited to|thrilled to|express my interest|pleased to apply|interest in|applying)\b", text_lower))

    # 3. Body content (meaningful middle paragraphs or substantial text)
    paragraphs = [p.strip() for p in cover_letter_clean.split("\n") if p.strip()]
    has_body = (len(paragraphs) >= 2 or word_count >= 30) and word_count > 0

    # 4. Closing content (e.g. "Sincerely", "Regards", "Best regards", "Thank you")
    has_closing = bool(re.search(r"\b(sincerely|regards|best regards|warm regards|warmly|respectfully|thank you|look forward)\b", text_lower))

    # 5. Candidate name / sign-off
    cand_name = str(candidate_profile.get("Full Name", "")).strip().lower()
    has_name_signoff = False
    if cand_name and cand_name in text_lower:
        has_name_signoff = True
    elif bool(re.search(r"(sincerely|regards|best regards|warm regards|warmly|respectfully)[\s\S]{1,60}$", text_lower)):
        has_name_signoff = True
    elif len(paragraphs) >= 3 and word_count >= 15:
        has_name_signoff = True

    structure_items = [has_greeting, has_opening, has_body, has_closing, has_name_signoff]
    structure_score = sum(4 for item in structure_items if item)

    if structure_score < 20:
        feedback.append("Improve the cover letter structure with a clear greeting, body and closing.")
    else:
        feedback.append("Excellent cover letter structure with all key components.")

    # ---------------------------------------------------------
    # 4. PROFESSIONAL LANGUAGE SCORE — 20 points
    # ---------------------------------------------------------
    found_prof_terms = sum(1 for term in PROFESSIONAL_KEYWORDS if term in text_lower)
    # 2 points per term found, capped at 20
    professionalism_score = min(20, found_prof_terms * 2)

    if professionalism_score < 15:
        feedback.append("Use more professional and job-focused language.")
    else:
        feedback.append("Effective use of professional language throughout the letter.")

    # ---------------------------------------------------------
    # 5. PERSONALIZATION SCORE — 10 points
    # ---------------------------------------------------------
    # Check: Candidate name, Education, Projects, Experience, Achievements
    personalization_fields = ["Full Name", "Education", "Projects", "Experience", "Achievements"]

    # Filter to only fields that actually contain information in candidate_profile
    active_fields = [
        f for f in personalization_fields
        if str(candidate_profile.get(f, "")).strip() and str(candidate_profile.get(f, "")).strip().lower() not in ("not provided", "none", "n/a")
    ]

    if not active_fields:
        personalization_score = 0
    else:
        matched_fields = 0
        for f in active_fields:
            val = str(candidate_profile.get(f, ""))
            if f == "Full Name":
                cand_clean = val.strip().lower()
                first_name = cand_clean.split()[0] if cand_clean else ""
                if cand_clean in text_lower or (first_name and first_name in text_lower):
                    matched_fields += 1
            else:
                if _field_in_text(val, text_lower):
                    matched_fields += 1

        personalization_score = round((matched_fields / len(active_fields)) * 10)
        personalization_score = max(0, min(10, personalization_score))

    if personalization_score < 7:
        feedback.append("Add more candidate-specific details such as projects, education or experience.")
    else:
        feedback.append("Good personalization using candidate-specific information.")

    # ---------------------------------------------------------
    # 6. TOTAL SCORE
    # ---------------------------------------------------------
    total_score = round(
        word_count_score +
        keyword_score +
        structure_score +
        professionalism_score +
        personalization_score
    )
    total_score = max(0, min(100, total_score))

    # Overarching high score feedback
    if total_score >= 80:
        feedback.append("Good quality cover letter with strong relevance and personalization.")

    return QualityScoreResult(
        total_score=total_score,
        word_count_score=word_count_score,
        keyword_score=keyword_score,
        structure_score=structure_score,
        professionalism_score=professionalism_score,
        personalization_score=personalization_score,
        feedback=feedback,
        word_count=word_count
    )
