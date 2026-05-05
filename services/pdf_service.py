# services/pdf_service.py

import fitz  # PyMuPDF

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        text += f"\n--- Page {page_num + 1} ---\n"
        text += page_text

    return text