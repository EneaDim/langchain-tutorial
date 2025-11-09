from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import AnalyzeResult
from app.services.cache import get_cached, set_cached
from app.models.db import SessionLocal, engine
from app.models.job import Job
from pydantic import BaseModel
from pypdf import PdfReader
from collections import Counter
import re, json

router = APIRouter(prefix="/analyze", tags=["analyze"])

STOPWORDS = set(("the a an of to and in is on for with as by at from that this "
                 "are it be or was were has have had not but if into about you your "
                 "we they i he she them their our us can will shall do does did "
                 "suo sua dei delle degli che per con una un di il lo la le gli "
                 "e non ma se su da nel nei nelle").split())

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
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(parts[:sentences]).strip() or (text[:300] + ("..." if len(text) > 300 else ""))

MAX_MB = 25  # semplice guard-rail; puoi spostarlo in settings/env

@router.post("", response_model=AnalyzeResult)
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > MAX_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_MB} MB)")

    cache_key = f"analyze:{file.filename}:{len(content)}"
    cached = get_cached(cache_key)
    if cached:
        data = json.loads(cached)
        # write-through su DB se row mancante
        try:
            from sqlalchemy import text
            with SessionLocal() as db:
                exists = db.execute(text("SELECT 1 FROM jobs WHERE filename=:f LIMIT 1"), {"f": file.filename}).first()
                if not exists:
                    db.execute(
                        text("INSERT INTO jobs (filename, keywords, summary) VALUES (:f, :k, :s)"),
                        {"f": file.filename, "k": json.dumps(data["keywords"]), "s": data["summary"]},
                    )
                    db.commit()
        except Exception:
            pass
        return AnalyzeResult(**data)

    text_str = extract_text_from_pdf(content)
    kws = keyword_extract(text_str)
    summary = summarize(text_str)
    result = AnalyzeResult(pages=text_str.count("\f")+1 if text_str else 0, summary=summary, keywords=kws)

    Job.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.add(Job(filename=file.filename, keywords=json.dumps(kws), summary=summary))
        db.commit()

    set_cached(cache_key, result.model_dump_json(), ttl=600)
    return result
