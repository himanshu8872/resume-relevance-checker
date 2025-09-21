import fitz  # This is the PyMuPDF library
import docx # This is the python-docx library
import os

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF {os.path.basename(file_path)}: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX {os.path.basename(file_path)}: {e}")
        return None

def parse_resume(file_path):
    """
    Parses a resume file (PDF or DOCX) and returns its text content.
    """
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print(f"Unsupported file format: {os.path.basename(file_path)}")
        return None