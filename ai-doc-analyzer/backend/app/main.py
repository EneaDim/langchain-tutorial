from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader
from collections import Counter
import re

app = FastAPI(title="AI-Doc Analyzer API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STOPWORDS = set(("the a an of to and in is on for with as by at from that this "
                 "are it be or was were has have had not but if into about you your "
                 "we they i he she them their our us can will shall do does did "
                 "suo sua dei delle degli che per con una un di il lo la le gli "
                 "e non ma se su da nel nei nelle").split())

class AnalyzeResult(BaseModel):
    pages: int
    summary: str
    keywords: list[str]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    from io import BytesIO
    reader = PdfReader(BytesIO(file_bytes))
    text = []
    for page in reader.pages:
        try:
            text.append(page.extract_text() or "")
        except Exception:
            text.append("")
    return "\n".join(text)

def keyword_extract(text: str, k: int = 10) -> list[str]:
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9']+", text.lower())
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(k)]

def summarize(text: str, sentences: int = 3) -> str:
    # super semplice: prime N frasi pulite
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(parts[:sentences]).strip() or (text[:300] + ("..." if len(text) > 300 else ""))

@app.post("/analyze", response_model=AnalyzeResult)
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(content)
    kws = keyword_extract(text)
    summary = summarize(text)
    return AnalyzeResult(pages=text.count("\f")+1 if text else 0, summary=summary, keywords=kws)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
