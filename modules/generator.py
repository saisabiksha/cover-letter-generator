"""Cover letter generator module supporting multiple writing styles."""


def _clean_str(val) -> str:
    """Helper to sanitize and clean profile strings."""
    if not val or not isinstance(val, str):
        return ""
    cleaned = val.strip()
    if cleaned.lower() in ("not provided", "none", "n/a", "null"):
        return ""
    return cleaned


def _format_skills_list(skills: list) -> str:
    """Format a list of skills into natural English (e.g. 'Python, SQL and Docker')."""
    if not skills:
        return ""
    if len(skills) == 1:
        return skills[0]
    if len(skills) == 2:
        return f"{skills[0]} and {skills[1]}"
    return ", ".join(skills[:-1]) + f", and {skills[-1]}"


def generate_cover_letter(candidate_profile: dict, job_data: dict, matched_skills: list, style: str = "Professional") -> str:
    """Generate a personalized cover letter based on candidate and job data.

    Supports three writing styles:
    - Standard: Simple, clear, formal, beginner-friendly language.
    - Professional: Polished, corporate, confident, formal language.
    - Creative: Engaging, professional, expressive yet appropriate.

    Structure:
    1. Greeting
    2. Opening paragraph
    3. Body paragraph(s) (skills, experience/projects, achievements)
    4. Closing paragraph
    5. Sign-off with candidate name
    """
    candidate_profile = candidate_profile or {}
    job_data = job_data or {}
    matched_skills = matched_skills or []

    # Extract and clean candidate information
    name = _clean_str(candidate_profile.get("Full Name")) or "Candidate"
    education = _clean_str(candidate_profile.get("Education"))
    skills_raw = _clean_str(candidate_profile.get("Skills"))
    projects = _clean_str(candidate_profile.get("Projects"))
    experience = _clean_str(candidate_profile.get("Experience"))
    achievements = _clean_str(candidate_profile.get("Achievements"))

    # Extract and clean job information
    job_title = _clean_str(job_data.get("Job Title")) or "the advertised position"
    company_name = _clean_str(job_data.get("Company Name")) or "your company"

    # Determine skills text representation
    if matched_skills:
        skills_text = _format_skills_list(matched_skills)
    elif skills_raw:
        # Fall back to candidate's stated skills if matched_skills is empty
        skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
        skills_text = _format_skills_list(skills_list[:4])
    else:
        skills_text = ""

    # Normalize style selection
    style_choice = (style or "Professional").strip().capitalize()

    # -------------------------------------------------------------------------
    # 1. Standard Style (Simple, clear, formal, beginner-friendly)
    # -------------------------------------------------------------------------
    if style_choice == "Standard":
        # Greeting
        greeting = f"Dear Hiring Manager at {company_name},"

        # Opening paragraph
        if education:
            opening = (
                f"I am writing to express my interest in the {job_title} position at {company_name}. "
                f"With my academic background in {education}, I am excited about the opportunity to "
                f"contribute my skills and enthusiasm to your organization."
            )
        else:
            opening = (
                f"I am writing to express my strong interest in the {job_title} position at {company_name}. "
                f"I believe my background and technical abilities make me a solid candidate for this role."
            )

        # Body paragraph construction
        body_parts = []
        if skills_text:
            body_parts.append(
                f"I have developed hands-on technical proficiency in {skills_text}, which aligns well "
                f"with the core requirements for the {job_title} role."
            )
        if experience and projects:
            body_parts.append(
                f"Through my experience ({experience}) and practical projects such as {projects}, "
                f"I have learned how to solve practical problems effectively."
            )
        elif experience:
            body_parts.append(
                f"In my previous work ({experience}), I developed practical skills and learned "
                f"to collaborate effectively in a professional setting."
            )
        elif projects:
            body_parts.append(
                f"My practical project work includes {projects}, which provided me with valuable "
                f"hands-on problem-solving experience."
            )

        if achievements:
            body_parts.append(
                f"Furthermore, I am proud of achieving {achievements}, which reflects my commitment "
                f"and ability to succeed under challenge."
            )

        body = " ".join(body_parts) if body_parts else (
            f"I am eager to apply my foundational skills and dedication to deliver meaningful results for {company_name}."
        )

        # Closing paragraph
        closing = (
            f"Thank you for considering my application for the {job_title} position. "
            f"I look forward to the possibility of discussing how my qualifications match the needs of {company_name}."
        )

        # Sign-off
        sign_off = f"Sincerely,\n{name}"

    # -------------------------------------------------------------------------
    # 2. Professional Style (Polished, corporate, confident, formal)
    # -------------------------------------------------------------------------
    elif style_choice == "Professional":
        # Greeting
        greeting = f"Dear Hiring Committee at {company_name},"

        # Opening paragraph
        if education:
            opening = (
                f"Please accept this letter as formal application for the {job_title} role at {company_name}. "
                f"Building upon a rigorous educational foundation in {education}, I offer a goal-oriented "
                f"approach and technical competencies well-suited to support your team's strategic initiatives."
            )
        else:
            opening = (
                f"Please accept this letter as formal application for the {job_title} position at {company_name}. "
                f"I offer a results-driven mindset and proven technical competencies tailored to advance "
                f"your organization's high standards."
            )

        # Body paragraph construction
        body_parts = []
        if skills_text:
            body_parts.append(
                f"A review of the role requirements highlights the critical importance of expertise in {skills_text}. "
                f"My background directly demonstrates core competence in these areas, positioning me to deliver "
                f"immediate value to your deliverables."
            )
        if experience and projects:
            body_parts.append(
                f"My professional record features {experience}, complemented by notable initiatives including {projects}. "
                f"These experiences have refined my capacity for systematic problem solving and cross-functional execution."
            )
        elif experience:
            body_parts.append(
                f"During my background in {experience}, I consistently demonstrated accountability, analytical precision, "
                f"and technical rigor."
            )
        elif projects:
            body_parts.append(
                f"Key projects such as {projects} highlight my ability to translate technical concepts into reliable, "
                f"scalable outcomes."
            )

        if achievements:
            body_parts.append(
                f"Additionally, my accomplishments include {achievements}, demonstrating a sustained dedication "
                f"to excellence and continuous improvement."
            )

        body = " ".join(body_parts) if body_parts else (
            f"I am prepared to leverage my technical foundation and professional dedication to contribute directly to {company_name}."
        )

        # Closing paragraph
        closing = (
            f"I welcome the opportunity to discuss in greater detail how my qualifications and technical capabilities "
            f"can contribute to the continued success of {company_name}. Thank you for your time and consideration."
        )

        # Sign-off
        sign_off = f"Best regards,\n{name}"

    # -------------------------------------------------------------------------
    # 3. Creative Style (Engaging, professional, expressive, modern)
    # -------------------------------------------------------------------------
    else:  # Creative
        # Greeting
        greeting = f"Dear {company_name} Team,"

        # Opening paragraph
        if education:
            opening = (
                f"I was thrilled to discover the {job_title} opportunity at {company_name}! "
                f"Combining my educational background in {education} with an active curiosity for innovation, "
                f"I am eager to bring fresh perspectives, energy, and hands-on problem-solving to your team."
            )
        else:
            opening = (
                f"I was inspired to see the {job_title} opening at {company_name}! "
                f"With a passion for modern technology and dynamic problem-solving, I am excited about "
                f"the prospect of collaborating with such a forward-thinking team."
            )

        # Body paragraph construction
        body_parts = []
        if skills_text:
            body_parts.append(
                f"What excites me most about this opportunity is leveraging tools like {skills_text} to craft "
                f"creative, impactful solutions that address complex challenges."
            )
        if experience and projects:
            body_parts.append(
                f"Through my experience ({experience}) and hands-on work with {projects}, I have embraced building "
                f"ideas into meaningful, functioning products."
            )
        elif experience:
            body_parts.append(
                f"My journey includes {experience}, which deepened my drive to solve problems with curiosity and persistence."
            )
        elif projects:
            body_parts.append(
                f"Engaging in projects like {projects} has allowed me to turn creative curiosity into solid, working technology."
            )

        if achievements:
            body_parts.append(
                f"I am especially proud of {achievements}, an achievement that fuels my desire to keep learning "
                f"and making an impact."
            )

        body = " ".join(body_parts) if body_parts else (
            f"I am excited to bring my energy, innovative mindset, and strong work ethic to {company_name}."
        )

        # Closing paragraph
        closing = (
            f"I would love the opportunity to chat about how my enthusiasm and technical skills can support "
            f"{company_name}'s future milestones. Thank you for taking the time to review my story!"
        )

        # Sign-off
        sign_off = f"Warmly,\n{name}"

    # Combine all sections with clean double-spacing
    cover_letter = f"{greeting}\n\n{opening}\n\n{body}\n\n{closing}\n\n{sign_off}"
    return cover_letter
