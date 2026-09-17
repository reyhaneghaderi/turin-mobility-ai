from pathlib import Path
from pypdf import PdfReader


# Project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Folder containing the PDFs
PDF_FOLDER = PROJECT_ROOT / "documents"


def extract_pdf_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Find all PDF files
pdf_files = list(PDF_FOLDER.glob("*.pdf"))