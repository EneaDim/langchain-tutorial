from pypdf import PdfReader
from pdfminer_high_level import extract_text as pdfminer_text  # noqa: keep consistent import name
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from docx import Document as DocxDocument
from typing import List, Dict

# fix: pdfminer import path used earlier
from pdfminer.high_level import extract_text as pdfminer_text

def extract_text_from_pdf(data: bytes) -> str:
    try:
        return pdfminer_text(fp=data)
    except Exception:
        # pypdf fallback
        import io
        reader = PdfReader(io.BytesIO(data))
        return "\n".join([p.extract_text() or "" for page in reader.pages for p in [page]])

def extract_text_from_docx(data: bytes) -> str:
    import io
    doc = DocxDocument(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_html(data: bytes) -> str:
    soup = BeautifulSoup(data, "lxml")
    return soup.get_text(separator="\n")

def extract_text_from_md(data: bytes) -> str:
    md = MarkdownIt()
    html = md.render(data.decode("utf-8", errors="ignore"))
    return BeautifulSoup(html, "lxml").get_text(separator="\n")

def to_chunks(text: str, max_chars: int = 2000, overlap: int = 200) -> List[Dict]:
    chunks = []
    i = 0
    while i < len(text):
        end = min(len(text), i + max_chars)
        chunks.append({"text": text[i:end], "start": i, "end": end})
        i = end - overlap
        if i < 0: i = 0
    return chunks
