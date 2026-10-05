# AI Cover Letter Generator

An NLP-based web application that analyzes job descriptions, matches candidate skills, generates personalized cover letters, scores the generated letter, and allows TXT/PDF export.

## Problem Statement

Job seekers often spend significant time creating different cover letters for different job applications. Crafting a tailored, professional letter for every role can be repetitive and time-consuming. The AI Cover Letter Generator helps automate and personalize this process by aligning candidate qualifications directly with target job requirements.

## Objective

The main objectives of this project are:
- Analyze job descriptions using Natural Language Processing (NLP) techniques.
- Extract important keywords and key responsibilities.
- Match candidate skills with specific job requirements.
- Generate personalized cover letters tailored to individual applications.
- Provide multiple writing styles (Standard, Professional, and Creative).
- Evaluate cover letter quality across multiple objective metrics.
- Export cover letters in convenient formats (TXT and PDF).

## Features

- **Candidate Profile Input**: Capture candidate details including education, skills, projects, experience, and achievements.
- **Job Description Analysis**: Parse target roles, company names, and raw job descriptions.
- **NLP Keyword Extraction**: Identify the most frequent and prominent terms from the job posting.
- **Skill Matching**: Compare candidate skills against a technical skill catalog.
- **Match Percentage**: Calculate relevance score with clear visual progress feedback.
- **Personalized Cover Letter Generation**: Dynamic, template-based generation that naturally incorporates profile details without awkward empty fields.
- **Three Writing Styles**: Choose between Standard, Professional, and Creative tones.
- **Cover Letter Quality Scoring**: Objective 100-point scoring system assessing length, keywords, structure, language, and personalization.
- **Scoring Test Mode**: Dedicated sandbox to test the quality scoring engine with any custom letter text.
- **TXT Export**: Instant one-click download for raw text format.
- **PDF Export**: In-memory, publication-ready PDF creation using ReportLab.
- **Empty Input Validation**: Safe input checking with clear user warnings to prevent errors or crashes.
- **Streamlit Web Interface**: Clean, wide-layout responsive UI designed for simplicity and ease of use.

## Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python** | Application development |
| **Streamlit** | Web interface |
| **NLTK** | Natural Language Processing |
| **Pandas** | Data processing |
| **ReportLab** | PDF generation |

## NLP Techniques

The application uses core NLP techniques provided by Python and NLTK:
- **Text Preprocessing**: Normalizing raw input text into a clean format.
- **Lowercase Conversion**: Converting characters to lowercase to ensure uniform, case-insensitive keyword comparisons.
- **Tokenization**: Segmenting continuous text into individual word units.
- **Stopword Removal**: Eliminating non-informative grammatical words (e.g., *the*, *and*, *is*) using standard English stopword lists.
- **Punctuation Removal**: Filtering out symbols, punctuation, and non-alphabetic tokens.
- **Keyword Extraction**: Extracting key terms with a minimum character threshold.
- **Word Frequency Analysis**: Using frequency distribution to rank the most relevant terms in a job description.

## How Skill Matching Works

1. **Candidate skills are collected**: The user enters their skills (comma-separated or listed) in the profile section.
2. **Job description keywords are extracted**: The job posting is preprocessed and tokenized.
3. **Relevant technical skills are identified**: The text is filtered against a predefined catalog of technical skills, recognizing both single-word and multi-word terms (e.g., *Machine Learning*, *Data Science*).
4. **Candidate skills are compared with job skills**: Each identified job skill is checked against normalized candidate skills.
5. **Matched and missing skills are displayed**: Skills are separated into matched (highlighted with ✅) and missing (highlighted with ⚠️).
6. **Match percentage is calculated**:
   $$\text{Match Percentage} = \left(\frac{\text{Number of Matched Relevant Skills}}{\text{Total Relevant Job Skills}}\right) \times 100$$
   *(Defaults safely to 0% if no technical skills are detected).*

## Cover Letter Generation

The application uses a **template-based generation approach** to build structured, authentic cover letters.

The generator personalizes the letter by incorporating:
- Candidate information (name, contact information)
- Job title
- Target company name
- Matched skills
- Candidate education
- Practical projects
- Professional experience
- Notable achievements

*Note: The generator uses pure Python template logic and string formatting. No external Generative AI API (such as OpenAI or Gemini) is currently used, ensuring offline reliability, high speed, and zero API costs.*

## Quality Scoring

The generated cover letter is evaluated across five objective categories totaling **100 points**:

- **Word Count (20 points)**: Checks whether the letter falls within the ideal professional range of 150–400 words.
- **Keyword Match (30 points)**: Verifies how many of the target job skills actually appear in the letter.
- **Structure (20 points)**: Checks for the presence of a greeting, opening paragraph, body content, closing statement, and sign-off with candidate name (4 points each).
- **Professional Language (20 points)**: Assesses the presence of formal industry terminology (e.g., *experience*, *qualifications*, *contribute*, *opportunity*).
- **Personalization (10 points)**: Verifies that candidate-specific background details (education, projects, experience, achievements) appear in the text.

The system also provides actionable feedback tips for any areas scoring below full marks.

## Export Options

- **TXT Download**: Export the letter as a plain `.txt` file for easy copying or manual editing.
- **PDF Download**: Export an in-memory, formatted `.pdf` document with professional margins and clean typography using ReportLab.

## Project Structure

```text
AI-Cover-Letter-Generator/
│
├── app.py                  # Main Streamlit web application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
├── data/
│   ├── templates.json      # Cover letter templates and style configurations
│   └── sample_data.json    # Sample profile and job description data for testing
│
├── modules/
│   ├── __init__.py         # Package initializer
│   ├── nlp_processing.py   # Tokenization, cleaning, and keyword extraction
│   ├── skill_matching.py   # Skill extraction and matching algorithms
│   ├── generator.py        # Multi-style personalized cover letter generation
│   ├── scoring.py          # 100-point multi-metric quality evaluation engine
│   └── pdf_export.py       # In-memory PDF document generation with ReportLab
│
└── outputs/                # Directory for generated cover letter exports
```

### Important Files
- `app.py`: Streamlit front-end coordinating all sections, state management, and user interaction.
- `modules/nlp_processing.py`: Handles text normalization, tokenization, stop-word removal, and keyword counting.
- `modules/skill_matching.py`: Manages the technical skill catalog and computes skill overlap.
- `modules/generator.py`: Generates complete cover letters in Standard, Professional, or Creative styles.
- `modules/scoring.py`: Evaluates word count, keywords, structure, language, and personalization.
- `modules/pdf_export.py`: Renders the letter into downloadable PDF format using ReportLab.

## Installation

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run app.py
```
