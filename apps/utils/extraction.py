from docx import Document
from PyPDF2 import PdfReader
import os

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    # Fichiers .txt
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    # Fichiers .pdf
    elif ext == ".pdf":
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    # Fichiers .docx
    elif ext in [".docx"]:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return ""
