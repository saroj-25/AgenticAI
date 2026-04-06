from pathlib import Path
from pypdf import PdfReader
from docx import Document

## function to read pdf 
def read_pdf(file_path:str) -> str: 
    reader = PdfReader(file_path)
    texts = []

    for page in reader.pages: 
        page_text = page.extract_text() or ""
        texts.append(page_text)

    return "\n".join(texts).strip()

def  read_docx(file_path:str) -> str: 
    docs = Document()
    return "\n".join([p.text for p in docs.paragraphs]).strip()

def read_cv(file_path : str) -> str: 
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return read_pdf(file_path)
    if suffix == ".docx": 
        return read_docx(file_path)
    
    raise ValueError(f"Unsupported file type {suffix}")


