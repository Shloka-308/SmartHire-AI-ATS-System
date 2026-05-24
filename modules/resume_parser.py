import pdfplumber
import fitz
from docx import Document
import os
def extract_text_from_pdf(pdf_path):
    txt=""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extrected = page.extract_text()
                if extrected:
                    txt += extrected + "\n"
    except:
        doc = fitz.open(pdf_path)
        for page in doc:
            txt += page.get_text()
    return txt

def extract_text_from_docx(docx_path):
    doc= Document(docx_path)
    txt = "\n".join([para.text for para in doc.paragraphs])
    return txt

def parse_resume(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return extract_text_from_pdf(file_path)
        elif ext==".docx":
            return extract_text_from_docx(file_path)
        else:
            return "Unsupported File Format"
