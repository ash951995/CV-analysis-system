# parser/docx_parser.py
from docx import Document

def extract_text_from_docx(docx_path):
    """
    Extracts text from a DOCX file.

    Args:
        docx_path (str): Path to the DOCX file.

    Returns:
        str: Extracted text from the DOCX.
    """
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"  # Extract text from each paragraph
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

    return text.strip()
