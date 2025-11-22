import pdfplumber
from typing import Optional
import os


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF resume file.
    
    Args:
        file_path: Path to the PDF file
    
    Returns:
        Extracted text content
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")


def extract_name_from_resume(text: str) -> Optional[str]:
    """
    Attempt to extract candidate name from resume text.
    Usually the first line or first few words.
    """
    lines = text.split('\n')
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line and len(line.split()) <= 4:  # Name is usually short
            # Basic validation: contains letters, not all caps (unless it's a name)
            if any(c.isalpha() for c in line):
                return line
    return None


def extract_email_from_resume(text: str) -> Optional[str]:
    """
    Extract email address from resume text using regex.
    """
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

