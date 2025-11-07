# Smart Report Writer

**Production-ready, modular SaaS** for analyzing mixed-format inputs and generating polished reports using selectable LLM providers. First-class support for **Llama 3** and **Qwen 2** (via Ollama). Optional adapters for **OpenAI** and **vLLM**.

---

## What it does

- Ingests and normalizes many file types:
  - **Documents:** PDF, DOCX, TXT, RTF, Markdown, HTML, LaTeX, PPTX, EPUB
  - **Tabular/Data:** CSV, TSV, XLS/XLSX, JSON, JSONL, XML, Parquet
  - **Code:** Python, JS/TS, Java, C/C++, Go, Rust, C#, SQL, Shell (auto-detect)
  - **Emails/Web:** EML, MBOX, optional URL fetch
  - **Archives:** ZIP, TAR, TAR.GZ (safe, recursive with limits)
  - **Media:** Images (OCR), Audio (speech-to-text)
  - **DB dumps (optional):** SQLite files, SQL scripts (feature-flag)
- Analyzes with **LangChain** chains specialized per content kind (document, tabular, code).
- Generates reports using **Jinja2** templates (HTML by default; PDF/DOCX optional).
- Offers **developer** and **user** modes, REST API + optional SSE/WebSocket for progress.
- Ships with **Docker Compose**, **GitHub Actions CI/CD**, and production hardening.

---

## Highlights

- **LLM selection at runtime**  
  Choose provider/model per request or via configuration. Defaults:
  - Provider: LLAMA_OLLAMA  
  - Model: llama3:8b-instruct  
  Secondary:
  - Provider: QWEN_OLLAMA  
  - Model: qwen2:7b-instruct

- **Clean architecture**  
  Ingestion → Analysis → Generation → Export. Strict Pydantic models, idempotent pipelines, audit trail.

- **Observability**  
  Health endpoints, Prometheus metrics, optional OpenTelemetry traces.

- **Security**  
  Read-only containers in prod, S3 pre-signed URLs, upload caps, archive safety, filename/path validation, (optional) antivirus hook.

---

## Repository layout (key paths)

- `api/` — FastAPI service (uploads, generate, jobs, templates, LLM info)
- `worker/` — Celery worker (analysis + rendering pipeline)
- `smart_report_writer/core/`
  - `ingestion/` — storage, MIME detection, extractors, validators, repo
  - `analysis/` — prompts, chains, provider adapters
  - `generation/` — Jinja2 rendering, exporters, pipeline
  - `templates/` — Jinja templates + metadata
  - `models/` — Pydantic models (domain, requests, responses, settings, llm)
  - `utils/` — logging, metrics, retry, ids, time, security
- `ui/streamlit/` — operations UI (upload → generate → status)
- `ui/react/` — production UI (upload, generate, status)
- `config/` — app and template configuration
- `docker/` — Dockerfiles for api/worker/ui
- `docs/` — user/dev/ops docs + ADRs
- `.github/workflows/` — CI/CD pipelines

---

## Running the stack (conceptual)

The system is containerized and orchestrated with Docker Compose:
- API on a web port with health checks
- Worker with Celery/Redis
- Postgres for metadata
- MinIO (S3-compatible) for uploads/artifacts
- Optional Ollama/vLLM/OpenAI for model inference
- Streamlit and React frontends

If you prefer local LLMs, run an Ollama service and ensure the default models are available. If you prefer managed providers, configure the relevant API credentials and base URLs.

> Note: This README intentionally avoids embedding shell blocks. See the project documentation for exact command lines.

---

## Configuration (environment overview)

- **App:** `APP_ENV`, `API_RATE_LIMIT_PER_MIN`
- **Database:** `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- **Redis:** `REDIS_URL`
- **S3/MinIO:** `S3_ENDPOINT_URL`, `S3_REGION`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_SECURE`, `S3_SERVER_SIDE_ENCRYPTION`
- **Providers & Models:**  
  `PROVIDER_DEFAULT`, `MODEL_DEFAULT`, `SECONDARY_PROVIDER_DEFAULT`, `SECONDARY_MODEL_DEFAULT`  
  `OLLAMA_BASE_URL`, `VLLM_ENDPOINT`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`
- **Features:** `FEATURE_OCR`, `FEATURE_STT`, `FEATURE_URL_FETCH`, `FEATURE_DB_DUMPS`
- **CORS/Security:** `ALLOWED_ORIGINS`, optional `JWT_PUBLIC_KEY_BASE64`, `JWT_AUDIENCE`, `OIDC_ISSUER`
- **Observability:** `PROMETHEUS_MULTIPROC_DIR`, `OTEL_EXPORTER_OTLP_ENDPOINT`

All defaults are documented in `.env.example`.

---

## Data flow

1. **Upload & classify**  
   File arrives → MIME sniff → extension verification → safety checks (size, traversal, archives) → content kind determined → metadata persisted → stored to S3/MinIO.

2. **Configure & generate**  
   Client selects template + provider/model (or uses defaults). API enqueues a job with idempotency key.

3. **Analyze & render**  
   Worker picks up job → content-kind specific chain (document/tabular/code) → Jinja template → artifact (HTML or PDF).

4. **Download & review**  
   Artifact stored with pre-signed URL; UI displays status and provides a download link.

---

## API overview

- `POST /v1/uploads` → returns document id, content kind, signed URL  
- `POST /v1/generate` → starts a job and returns a job id  
- `GET /v1/jobs/{job_id}` → job status  
- `GET /v1/jobs/{job_id}/artifact` → artifact download link  
- `GET /v1/templates` → templates catalog  
- `GET /v1/llm/providers` and `/v1/llm/defaults` → available providers and defaults

Standard response envelope: `{ data, error, meta }`.

---

## Templates

- Jinja2 templates in `smart_report_writer/core/templates`
- Template metadata in `config/templates.yml`
- Built-ins:
  - `executive_summary` (documents)
  - `technical_report` (documents)
  - `compliance_summary` (documents)
  - `dataset_profile` (tabular)
  - `code_overview` (code)
- Exporters: HTML (default) and PDF (WeasyPrint)

---

## Frontends

- **Streamlit (ops focus)**: simple flows to upload, pick template, start job, and poll status.
- **React (product UI)**: Tailwind-based, accessible, responsive; includes uploader, generator, status pages; SSE/WebSocket ready.

---

## Quality & Security

- **CI:** linting, type checks, tests, and Docker build (GitHub Actions)  
- **CD:** multi-arch image builds on tags  
- **Security:** image scanning, read-only containers in prod overlays, strict CORS in production, validated filenames and archive traversal prevention

---

## Observability

- `/healthz`, `/readyz`
- Prometheus metrics (extendable)
- Optional OpenTelemetry exporter

---

## LLM providers

- **Primary:** Llama 3 and Qwen 2 via Ollama
- **Optional:** OpenAI and vLLM via adapters
- **Runtime overrides:** choose provider and model per request in `GenerateRequest.overrides`

If local models are not present, consult the docs to make them available (e.g., by pulling with your preferred tooling).

---

## Limitations & notes

- Some advanced extractors (e.g., complex LaTeX, PPTX, EPUB) are covered at a “practical default” level; refine extractor settings as needed for your domain.
- OCR/STT, URL fetch, and DB-dump support are behind feature flags for security and footprint reasons.
- The example pipeline provides end-to-end behavior; you can swap in production storage/DB/extractor implementations where required.

---

## Documentation index

- Getting started
- Architecture
- API
- Operations
- Prompts & Chains
- Templates
- UI Guide
- Troubleshooting
- ADRs (provider choice, storage layout)

All live under `docs/`.

---

## License & contribution

- **License:** MIT
- **Contributing:** open to PRs. Please keep docs and tests in sync with changes.

