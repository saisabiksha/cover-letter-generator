"""Export module for generating TXT and PDF versions of cover letters."""

from io import BytesIO
import html
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT


def create_pdf(cover_letter: str) -> bytes:
    """Generate a clean, professional PDF from cover letter text in memory.

    Parameters:
        cover_letter (str): The text content of the cover letter.

    Returns:
        bytes: Raw PDF bytes suitable for downloading or writing to file.
    """
    if not cover_letter or not isinstance(cover_letter, str):
        cover_letter = ""

    buffer = BytesIO()

    # Create document template with standard A4 margins (approx 0.75 in / 54 pt)
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom paragraph style for clean professional typography
    body_style = ParagraphStyle(
        "CoverLetterBody",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        textColor="#1F2937"
    )

    story = []

    # Process each paragraph
    for paragraph in cover_letter.split("\n"):
        cleaned = paragraph.strip()
        if cleaned:
            # Escape XML/HTML special characters (&, <, >) to prevent ReportLab XML markup errors
            safe_text = html.escape(cleaned)
            story.append(Paragraph(safe_text, body_style))
            story.append(Spacer(1, 10))

    # Build PDF into the in-memory buffer
    document.build(story)

    # Return raw PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
