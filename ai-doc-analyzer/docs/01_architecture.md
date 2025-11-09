# 🧠 AI-Doc Analyzer — System Architecture

AI-Doc Analyzer is a containerized web application that analyzes PDF documents using NLP.
It extracts **keywords**, generates a **summary**, and stores results in PostgreSQL, while caching in Redis.

## 1. High-Level Overview
UI (Streamlit) → FastAPI Backend → PostgreSQL + Redis


## 2. Components

| Component | Purpose | Tech |
|------------|----------|------|
| UI | Upload & display results | Streamlit |
| Backend | PDF & NLP logic | FastAPI |
| Database | Store jobs | PostgreSQL |
| Cache | Store cached analyses | Redis |
| CI/CD | Tests, build, deploy | GitHub Actions |
| Orchestration | Local stack | Docker Compose |

## 3. Data Flow
1. User uploads PDF in UI.
2. UI sends file to FastAPI `/analyze`.
3. Backend parses, extracts keywords, saves to DB, caches in Redis.
4. UI displays summary.
5. Next request → Redis HIT.

