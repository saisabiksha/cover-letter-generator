import streamlit as st
from modules.nlp_processing import extract_keywords
from modules.skill_matching import match_skills, extract_technical_skills
from modules.generator import generate_cover_letter
from modules.scoring import calculate_score
from modules.pdf_export import create_pdf

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Cover Letter Generator",
    page_icon="📝",
    layout="wide"
)

# ---------------------------------------------------------
# 12. Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.title("AI Cover Letter Generator")
    st.subheader("About")
    st.write(
        "An NLP-based application that analyzes job descriptions, "
        "matches candidate skills, generates personalized cover letters, "
        "scores the result, and provides export options."
    )
    st.divider()
    st.subheader("Technology")
    st.markdown(
        "- **Python**\n"
        "- **Streamlit**\n"
        "- **NLTK**\n"
        "- **Pandas**\n"
        "- **ReportLab**"
    )

# ---------------------------------------------------------
# 2. Main Title Section
# ---------------------------------------------------------
st.title("📝 AI Cover Letter Generator")
st.write(
    "Generate personalized professional cover letters "
    "based on your profile and target job."
)

st.divider()

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "candidate_profile" not in st.session_state:
    st.session_state["candidate_profile"] = None
if "job_data" not in st.session_state:
    st.session_state["job_data"] = None
if "job_received" not in st.session_state:
    st.session_state["job_received"] = False
if "extracted_keywords" not in st.session_state:
    st.session_state["extracted_keywords"] = []
if "skill_match_result" not in st.session_state:
    st.session_state["skill_match_result"] = None
if "generated_cover_letter" not in st.session_state:
    st.session_state["generated_cover_letter"] = ""
if "selected_style" not in st.session_state:
    st.session_state["selected_style"] = ""
if "quality_score_result" not in st.session_state:
    st.session_state["quality_score_result"] = None
if "test_score_result" not in st.session_state:
    st.session_state["test_score_result"] = None
if "custom_test_letter" not in st.session_state:
    st.session_state["custom_test_letter"] = ""

# ---------------------------------------------------------
# Section A: Candidate Profile
# ---------------------------------------------------------
st.header("👤 Candidate Profile")
st.write("Fill in your details below to build your candidate profile.")

col_name, col_email = st.columns(2)
with col_name:
    full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
with col_email:
    email = st.text_input("Email", placeholder="e.g. john.doe@example.com")

col_phone, col_edu = st.columns(2)
with col_phone:
    phone_number = st.text_input("Phone Number", placeholder="e.g. +1 555-123-4567")
with col_edu:
    education = st.text_input("Education", placeholder="e.g. B.Tech in Computer Science - XYZ University")

col_skills, col_proj = st.columns(2)
with col_skills:
    skills = st.text_area(
        "Skills",
        placeholder="e.g. Python, Machine Learning, SQL, Pandas, Git",
        height=100
    )
with col_proj:
    projects = st.text_area(
        "Projects",
        placeholder="e.g. Built a Movie Recommendation System using Python and Streamlit",
        height=100
    )

col_exp, col_ach = st.columns(2)
with col_exp:
    experience = st.text_area(
        "Experience",
        placeholder="e.g. 6-month Data Science Internship at Tech Corp",
        height=100
    )
with col_ach:
    achievements = st.text_area(
        "Achievements",
        placeholder="e.g. 1st place in University Hackathon 2024",
        height=100
    )

if st.button("Save Candidate Profile", use_container_width=True):
    candidate_profile = {
        "Full Name": full_name,
        "Email": email,
        "Phone Number": phone_number,
        "Education": education,
        "Skills": skills,
        "Projects": projects,
        "Experience": experience,
        "Achievements": achievements
    }
    st.session_state["candidate_profile"] = candidate_profile
    st.success("Candidate profile saved successfully.")

# Display Saved Profile Below Form
if st.session_state["candidate_profile"] is not None:
    with st.expander("Saved Candidate Profile Details", expanded=False):
        saved_profile = st.session_state["candidate_profile"]
        for key, value in saved_profile.items():
            display_val = value if value.strip() != "" else "Not provided"
            st.write(f"**{key}:** {display_val}")

st.divider()

# ---------------------------------------------------------
# Section B: Job Information
# ---------------------------------------------------------
st.header("💼 Job Information")
st.write("Enter the details of the job you are targeting.")

col_job_title, col_company = st.columns(2)
with col_job_title:
    job_title = st.text_input("Job Title", placeholder="e.g. Junior Data Scientist")
with col_company:
    company_name = st.text_input("Company Name", placeholder="e.g. Acme Corp")

job_description = st.text_area(
    "Job Description",
    placeholder="Paste the full job description here...",
    height=200
)

if st.button("Analyze Job Description", use_container_width=True):
    missing_fields = []
    if not job_title.strip():
        missing_fields.append("Job Title")
    if not company_name.strip():
        missing_fields.append("Company Name")
    if not job_description.strip():
        missing_fields.append("Job Description")

    if missing_fields:
        st.session_state["job_received"] = False
        st.warning(f"Please fill in the required field(s): {', '.join(missing_fields)}.")
    else:
        job_data = {
            "Job Title": job_title.strip(),
            "Company Name": company_name.strip(),
            "Job Description": job_description.strip()
        }

        # Step 4: NLP Keyword Extraction
        keywords = extract_keywords(job_description.strip())

        # Step 5: Skill Matching
        candidate_skills_source = ""
        if st.session_state["candidate_profile"] is not None:
            candidate_skills_source = st.session_state["candidate_profile"].get("Skills", "")
        if not candidate_skills_source.strip():
            candidate_skills_source = skills

        match_result = match_skills(candidate_skills_source, job_description.strip())

        st.session_state["job_data"] = job_data
        st.session_state["extracted_keywords"] = keywords
        st.session_state["skill_match_result"] = match_result
        st.session_state["job_received"] = True

# Display confirmation and entered Job Title & Company Name
if st.session_state["job_received"] and st.session_state["job_data"] is not None:
    st.success("Job description received successfully.")
    current_job = st.session_state["job_data"]
    st.info(f"Target Role: **{current_job['Job Title']}** at **{current_job['Company Name']}**")

    # ---------------------------------------------------------
    # Section C: Job Description Analysis (NLP)
    # ---------------------------------------------------------
    st.divider()
    st.header("🔍 Job Description Analysis")
    keywords = st.session_state.get("extracted_keywords", [])

    st.metric("Total Keywords Extracted", len(keywords))

    if keywords:
        st.write("Below are the top keywords identified from the job description:")
        cols = st.columns(4)
        for idx, kw in enumerate(keywords):
            cols[idx % 4].markdown(f"- **{kw}**")
    else:
        st.info("No significant keywords could be extracted from the text.")

    # ---------------------------------------------------------
    # Section D: Skill Matching
    # ---------------------------------------------------------
    st.divider()
    st.header("🎯 Skill Matching")

    match_result = st.session_state.get("skill_match_result")

    if match_result is not None:
        job_skills = match_result.job_skills
        matched_skills = match_result.matched_skills
        missing_skills = match_result.missing_skills
        match_percentage = match_result.match_percentage

        if not job_skills:
            st.info("No technical skills from our predefined catalog were detected in the job description. Please provide a more detailed job description containing technical requirements.")
        else:
            # Visual metrics for skill matching
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Match Percentage", f"{match_percentage}%")
            with col_m2:
                st.metric("Matched Skills", len(matched_skills))
            with col_m3:
                st.metric("Missing Skills", len(missing_skills))

            st.progress(match_percentage / 100.0)

            # Clean side-by-side display of matched and missing skills
            col_match, col_miss = st.columns(2)
            with col_match:
                st.subheader("Matched Skills")
                if matched_skills:
                    for s in matched_skills:
                        st.success(f"✅ {s}")
                else:
                    st.write("None matched yet.")

            with col_miss:
                st.subheader("Missing Skills")
                if missing_skills:
                    for s in missing_skills:
                        st.warning(f"⚠️ {s}")
                else:
                    st.success("You match all detected technical requirements!")

st.divider()

# ---------------------------------------------------------
# Section E: Cover Letter Generator
# ---------------------------------------------------------
st.header("✍️ Cover Letter Generator")
st.write("Select your desired writing style and generate a personalized cover letter.")

style_choice = st.selectbox(
    "Choose Writing Style",
    options=["Standard", "Professional", "Creative"],
    index=1
)

if st.button("Generate Cover Letter", use_container_width=True):
    current_profile = st.session_state.get("candidate_profile")
    if not current_profile and full_name.strip():
        current_profile = {
            "Full Name": full_name,
            "Email": email,
            "Phone Number": phone_number,
            "Education": education,
            "Skills": skills,
            "Projects": projects,
            "Experience": experience,
            "Achievements": achievements
        }
        st.session_state["candidate_profile"] = current_profile

    if not current_profile or not current_profile.get("Full Name", "").strip():
        st.warning("Please complete and save your Candidate Profile (with at least your Full Name) before generating a cover letter.")
    elif not st.session_state.get("job_data"):
        st.warning("Please enter and analyze Job Information before generating a cover letter.")
    elif st.session_state.get("skill_match_result") is None:
        st.warning("Please click 'Analyze Job Description' first so relevant skills can be processed.")
    else:
        job_info = st.session_state["job_data"]
        match_res = st.session_state["skill_match_result"]
        matched_skills_list = match_res.matched_skills

        generated_letter = generate_cover_letter(
            candidate_profile=current_profile,
            job_data=job_info,
            matched_skills=matched_skills_list,
            style=style_choice
        )

        score_res = calculate_score(
            cover_letter=generated_letter,
            job_skills=match_res.job_skills,
            candidate_profile=current_profile
        )

        st.session_state["generated_cover_letter"] = generated_letter
        st.session_state["selected_style"] = style_choice
        st.session_state["quality_score_result"] = score_res
        st.success("Cover letter generated successfully!")

# Display the generated cover letter inside a clean container
if st.session_state.get("generated_cover_letter"):
    with st.container():
        st.subheader(f"Generated Cover Letter ({st.session_state.get('selected_style', style_choice)} Style)")
        st.text_area(
            label="Cover Letter Content",
            value=st.session_state["generated_cover_letter"],
            height=380
        )

    # ---------------------------------------------------------
    # Section G: Export Options
    # ---------------------------------------------------------
    st.subheader("📥 Export Options")
    generated_text = st.session_state["generated_cover_letter"]

    col_txt, col_pdf = st.columns(2)
    with col_txt:
        st.download_button(
            label="Download TXT",
            data=generated_text,
            file_name="cover_letter.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_pdf:
        try:
            pdf_data = create_pdf(generated_text)
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="cover_letter.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as error:
            st.error(f"Could not generate PDF: {error}")

    # ---------------------------------------------------------
    # Section F: Quality Score
    # ---------------------------------------------------------
    st.divider()
    st.header("📊 Cover Letter Quality Score")

    score_result = st.session_state.get("quality_score_result")
    if score_result is not None:
        st.metric("Overall Score", f"{score_result.total_score} / 100")
        st.progress(score_result.total_score / 100.0)

        # Metric breakdown using st.metric()
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        with m_col1:
            st.metric("Word Count Score", f"{score_result.word_count_score} / 20", f"{score_result.word_count} words")
        with m_col2:
            st.metric("Keyword Match", f"{score_result.keyword_score} / 30")
        with m_col3:
            st.metric("Structure", f"{score_result.structure_score} / 20")
        with m_col4:
            st.metric("Prof. Language", f"{score_result.professionalism_score} / 20")
        with m_col5:
            st.metric("Personalization", f"{score_result.personalization_score} / 10")

        st.subheader("Evaluation & Feedback")
        for feedback_item in score_result.feedback:
            st.info(feedback_item)

# ---------------------------------------------------------
# 10. Scoring Test Mode Expander (Testing Feature)
# ---------------------------------------------------------
st.divider()
with st.expander("Scoring Test Mode"):
    st.write("Use this section to test how the quality scoring algorithm responds to any custom cover letter text.")
    use_custom = st.checkbox("Use custom cover letter for testing", key="use_custom_test_mode")

    if use_custom:
        custom_letter = st.text_area(
            "Test Cover Letter",
            value=st.session_state.get("custom_test_letter", ""),
            height=250,
            placeholder="Paste your custom cover letter text here to test scoring..."
        )

        if st.button("Test Score", use_container_width=True):
            test_job_skills = []
            if st.session_state.get("skill_match_result"):
                test_job_skills = st.session_state["skill_match_result"].job_skills
            elif st.session_state.get("job_data"):
                test_job_skills = extract_technical_skills(st.session_state["job_data"].get("Job Description", ""))

            test_profile = st.session_state.get("candidate_profile") or {
                "Full Name": full_name,
                "Email": email,
                "Phone Number": phone_number,
                "Education": education,
                "Skills": skills,
                "Projects": projects,
                "Experience": experience,
                "Achievements": achievements
            }

            test_score_res = calculate_score(
                cover_letter=custom_letter,
                job_skills=test_job_skills,
                candidate_profile=test_profile
            )

            st.session_state["test_score_result"] = test_score_res
            st.session_state["custom_test_letter"] = custom_letter

        if st.session_state.get("test_score_result") is not None:
            t_score = st.session_state["test_score_result"]
            st.markdown("#### Test Cover Letter Quality Score")
            st.metric("Test Overall Score", f"{t_score.total_score} / 100")
            st.progress(t_score.total_score / 100.0)

            tm_col1, tm_col2, tm_col3, tm_col4, tm_col5 = st.columns(5)
            with tm_col1:
                st.metric("Word Count Score", f"{t_score.word_count_score} / 20", f"{t_score.word_count} words")
            with tm_col2:
                st.metric("Keyword Match", f"{t_score.keyword_score} / 30")
            with tm_col3:
                st.metric("Structure", f"{t_score.structure_score} / 20")
            with tm_col4:
                st.metric("Prof. Language", f"{t_score.professionalism_score} / 20")
            with tm_col5:
                st.metric("Personalization", f"{t_score.personalization_score} / 10")

            st.write("**Evaluation & Feedback:**")
            for item in t_score.feedback:
                st.info(item)

# ---------------------------------------------------------
# 13. Footer
# ---------------------------------------------------------
st.divider()
st.caption("AI Cover Letter Generator | Python + NLP + Streamlit")
