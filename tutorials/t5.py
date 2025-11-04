#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
t5.py — Minimal, one-file RAG using LangChain + Ollama + Chroma (with auto-download)

What this script does on a single `python t5.py`:
1) Downloads a tiny, text-only corpus (a few HTTP RFCs) into ./docs/ if missing.
2) Loads those .txt files, chunks them, and builds/loads a persistent Chroma vector index in ./rag_index.
3) Runs a fixed question (overridable with env var Q) through a simple RAG chain:
   - Retrieve top-k relevant chunks.
   - Feed them as "CONTEXT" to an LLM (Ollama-backed) with a strict prompt.
   - Print the model's answer.

Why this setup?
- Pure text sources (RFCs) = easy to download and parse without extra dependencies.
- Ollama runs models locally; no external APIs required.
- Chroma provides an on-disk vector store, so subsequent runs are much faster.

Customize:
- Change URL list to target a different corpus of .txt files.
- Swap models with EMBED_MODEL / LLM_MODEL.
- Adjust chunk size/overlap/retriever k for your needs.
"""

import os
import sys
import shutil
from pathlib import Path
from urllib.request import urlopen

# ---- LangChain / Ollama imports
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader  # You can replace/add loaders for PDF/HTML, etc.
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# =========================
# Configuration (edit here)
# =========================

# Directory where downloaded documents will live. Keep it local and simple.
DOCS_DIR = Path("docs")

# Directory for Chroma's persisted index (so you don't re-embed on every run).
PERSIST_DIR = "rag_index"

# Default question (you can override it without editing the file by setting env var Q="...").
QUESTION = os.environ.get("Q", "What are the main differences between HTTP/1.1 and HTTP/2?")

# Extremely easy-to-download, text-only corpus (HTTP-related RFCs).
# Swap these with any public .txt links you want to use as your corpus.
URLS = [
    "https://www.rfc-editor.org/rfc/rfc9110.txt",  # HTTP Semantics
    "https://www.rfc-editor.org/rfc/rfc9111.txt",  # HTTP Caching
    "https://www.rfc-editor.org/rfc/rfc9112.txt",  # HTTP/1.1
    "https://www.rfc-editor.org/rfc/rfc7540.txt",  # HTTP/2
]

# Embedding and chat models served by Ollama. Change these if you prefer other local models.
EMBED_MODEL = "qwen3-embedding:0.6b"   # e.g., "bge-m3" if you've pulled it
LLM_MODEL   = "qwen2.5-coder:1.5b"     # e.g., "qwen2.5:latest" or "llama3.1:8b"

# =========================
# Utility: downloading data
# =========================

def ensure_dir(p: Path) -> None:
    """Create directory p (including parents) if it doesn't exist."""
    p.mkdir(parents=True, exist_ok=True)

def download_corpus() -> None:
    """
    Download each URL in URLS into DOCS_DIR.
    - Skips downloads if files already exist.
    - Fails fast if after the loop no files are present.
    """
    ensure_dir(DOCS_DIR)
    for url in URLS:
        dst = DOCS_DIR / url.split("/")[-1]
        # Idempotency: if file is already there and non-empty, don't re-download
        if dst.exists() and dst.stat().st_size > 0:
            continue
        try:
            print(f"[download] {url}")
            with urlopen(url) as r, open(dst, "wb") as f:
                shutil.copyfileobj(r, f)
        except Exception as e:
            # We keep going even if a single file fails; we just require at least one doc to exist at the end.
            print(f"[skip] {url} ({e})", file=sys.stderr)

    # Safety: verify we have at least one file in ./docs
    if not any(DOCS_DIR.glob("*.txt")):
        raise SystemExit("No .txt files in ./docs (download failed).")

# =======================================
# Step 1) Load documents from ./docs/*.txt
# =======================================

def load_docs():
    """
    Load all .txt files from DOCS_DIR using TextLoader.
    - Adds a 'source' metadata key to each Document for citation in the final answer.
    - Returns: list[Document]
    """
    files = sorted([p for p in DOCS_DIR.glob("*.txt") if p.is_file()])
    if not files:
        raise SystemExit("No .txt files found in ./docs. Did the download fail?")

    docs = []
    for p in files:
        try:
            # TextLoader is robust for .txt; for PDFs/HTML consider dedicated loaders (PyPDF, UnstructuredHTML, etc.)
            loader = TextLoader(str(p), encoding="utf-8")
            loaded = loader.load()
            for d in loaded:
                d.metadata = d.metadata or {}
                d.metadata["source"] = str(p)  # crucial for showing sources in the answer
            docs.extend(loaded)
        except Exception as e:
            # We skip files that fail to load rather than crashing the entire script
            print(f"[skip] {p} ({e})", file=sys.stderr)

    if not docs:
        raise SystemExit("Could not load any documents from ./docs.")
    return docs

# ============================================
# Step 2) Chunk documents (RAG-friendly pieces)
# ============================================

def chunk_docs(docs, size: int = 800, overlap: int = 100):
    """
    Split documents into overlapping chunks so retriever can match finer-grained relevance.
    - size: max characters per chunk
    - overlap: characters shared between adjacent chunks (helps with boundary continuity)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        add_start_index=True  # optionally track character index inside original doc
    )
    return splitter.split_documents(docs)

# ===================================================
# Step 3) Build or load a Chroma index (persisted DB)
# ===================================================

def build_or_load_index(chunks):
    """
    Create (or reuse) a persistent Chroma index.
    - If PERSIST_DIR already holds an index, we reload it to avoid re-embedding on every run.
    - Otherwise, we build from chunks and persist it on disk.
    """
    # Embedding function used by Chroma internally (calls Ollama locally)
    embed = OllamaEmbeddings(model=EMBED_MODEL)

    persist_path = Path(PERSIST_DIR)
    if persist_path.exists() and any(persist_path.iterdir()):
        # Fast path: use existing vectors on disk
        print(f"[index] Loading existing index from '{PERSIST_DIR}'")
        vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embed)
    else:
        # Cold start: compute embeddings and build the store
        print(f"[index] Creating new index in '{PERSIST_DIR}'")
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embed,
            persist_directory=PERSIST_DIR
        )
        # Note: Chroma persists automatically when using persist_directory
    return vectordb

# =======================================
# Step 4) Define the RAG prompt and chain
# =======================================

# A tight, retrieval-only instruction: the LLM must use ONLY the given context.
PROMPT = ChatPromptTemplate.from_template(
    "You are a technical assistant.\n"
    "Answer ONLY using the following CONTEXT and always cite file sources (from the 'source' metadata).\n"
    "If the information is not present in the context, say so explicitly.\n\n"
    "CONTEXT:\n{context}\n\nQUESTION: {question}\n"
    "ANSWER (concise, in English, with file references):"
)

def fmt_docs(docs) -> str:
    """
    Convert retrieved Documents into a readable, inline 'context' string:
    - Includes short previews and the 'source' file path for traceability.
    - Keep it simple: bullet list with a small snippet from each chunk.
    """
    out = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source", "unknown")
        # Keep a short preview to stay within prompt length while remaining informative
        preview = d.page_content[:800].replace("\n", " ")
        out.append(f"- [{i}] {src} :: {preview}")
    return "\n\n".join(out)

# ============
# Main driver
# ============

def main():
    # 0) Ensure corpus is available locally (idempotent download).
    download_corpus()

    # 1) Load and 2) Chunk
    docs = load_docs()
    chunks = chunk_docs(docs, size=800, overlap=100)

    # 3) Build or load the vector index (Chroma + OllamaEmbeddings)
    vectordb = build_or_load_index(chunks)

    # Create a retriever interface (k controls how many chunks will be passed to the LLM)
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # Initialize the local LLM via Ollama (temperature=0 for deterministic, factual responses)
    llm = ChatOllama(model=LLM_MODEL, temperature=0)

    # The chain:
    # - In parallel, construct "context" from retriever results and pass the original "question" through.
    # - Then apply the prompt template.
    # - Finally, call the chat model.
    rag = (
        RunnableParallel(
            context=lambda x: fmt_docs(retriever.invoke(x["question"])),
            question=RunnablePassthrough(),
        )
        | PROMPT
        | llm
    )

    # 4) Ask the fixed question (or the one from env var Q)
    print(f"[query] {QUESTION}\n")
    try:
        result = rag.invoke({"question": QUESTION})
        # Chat models in LangChain return an object with `.content`; fall back to string if needed.
        content = getattr(result, "content", result)
        print("\n=== ANSWER ===\n")
        print(content)
    except Exception as e:
        # Catch runtime errors (e.g., Ollama not running, models not pulled, etc.)
        print(f"Error while running RAG chain: {e}", file=sys.stderr)
        sys.exit(1)

# Standard Python entrypoint
if __name__ == "__main__":
    main()

