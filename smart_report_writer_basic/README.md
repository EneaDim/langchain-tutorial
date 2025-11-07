# Smart Report Writer (Modular, LangChain + Ollama)

A modular, production-style version of your compact Smart Report Writer. It:
- Loads heterogeneous inputs (docs/logs/tables/code),
- Summarizes each bucket with LangChain LCEL,
- Produces a board-ready Executive Summary,
- Optionally renders a DOCX via a template (`docxtpl`).

> Works locally with Ollama models. No external APIs required.

---

## Quickstart

### 1) Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running
- An Ollama model pulled, e.g.:

```bash
ollama pull llama3.2:latest
# or any other: qwen2.5-coder:1.5b, mistral:7b-instruct, etc.
```

### 2) Install

```bash
pip install -e .
# optional extras for better loaders (PDF, DOCX, HTML):
pip install .[all]
```

Environment overrides (optional):

```bash
export OLLAMA_MODEL="llama3.2:latest"
export OLLAMA_BASE_URL="http://localhost:11434"
export MODEL_TEMPERATURE="0.2"
export SRW_PER_FILE_CAP="12000"
export SRW_TOTAL_CAP="150000"
```

### 3) Prepare Inputs

Place your files in a folder, e.g. `data/`. Supported types:
- Text: `.txt`, `.md`, `.log`, `.yaml`, `.cfg`, `.ini`
- Tables: `.csv`, `.tsv`, `.xlsx`, `.xls`, `.json`
- Docs: `.html`, `.pdf`, `.docx`
- Code: `.py`, `.js`, `.ts`, `.java`, `.go`, `.rb`, `.rs`, `.cs`, `.cpp`, `.c`, `.h`

### 4) Run

```bash
smart-report-writer -i "data/**/*" --recursive --topic "Q4 Ops Review"
```

Outputs:
- `summary.md` — the board-ready Executive Summary
- `report.md` — detailed report with sections per bucket

### 5) Streaming (optional)

```bash
smart-report-writer -i "data/**/*" --recursive --stream
```

You’ll see the master synthesis stream live in the terminal.

### 6) DOCX Template (optional)

If you have a `.docx` template with placeholders (docxtpl), pass:

```bash
smart-report-writer -i "data/**/*" --recursive   --docx-template-file templates/exec_template.docx   --detailed-out out/report.docx
```

Placeholders filled (via `ctx_map`):
- `TOPIC`
- `EXEC_SUMMARY`
- `DOCS`
- `TABLES`
- `LOGS`
- `CODE`
- `SOURCES`

> Tip: If `--detailed-out` doesn’t end with `.docx`, we’ll change it to `.docx` for you.

---

## CLI Reference

```
smart-report-writer -i INPUTS [--recursive]
  [--topic TOPIC]
  [--summary-out summary.md]
  [--detailed-out report.md]
  [--model OLLAMA_MODEL]
  [--base-url OLLAMA_BASE_URL]
  [--temperature 0.2]
  [--per-file-cap 12000]
  [--total-cap 150000]
  [--docx-template-file TEMPLATE.docx]
  [--stream]
```

**Examples**

```bash
smart-report-writer -i "data/*.pdf" "data/*.csv"
smart-report-writer -i "data/**/*" --recursive --topic "USB-C PD"
smart-report-writer -i "logs/*.log" --per-file-cap 8000 --total-cap 100000
```

---

## Architecture

```
smart_report_writer/
  cli.py           # argparse; wires everything
  config.py        # defaults & Settings
  llm.py           # ChatOllama factory; streaming helper
  prompts.py       # Prompt templates (LangChain)
  loaders/         # file-type loaders
  pipeline/        # dataclasses, bucketing, chains, orchestration
  output/          # writers and Jinja2 templates
  demos/           # minimal LC demos (streaming, structured, routing)
```

- **LCEL everywhere**: `prompt | llm | parser`
- **Async where useful**: `.ainvoke()` with `tenacity` retries
- **Graceful optional deps**: PDFs/DOCX/HTML handled if libs available
- **Caps & truncation**: `...[truncated]...` marker

---

## Troubleshooting

- **Ollama connection error**: Ensure `ollama serve` is running; correct `--base-url`.
- **Model not found**: `ollama pull <model>`.
- **Missing optional loaders**: `pip install .[all]` (for `pdfplumber`, `docxtpl`, etc.).
- **Weird CSV delimiter**: CSV sniffer tries `, ; \t |` and falls back to comma.

---

## Demos

Run from repo root:

```bash
python -m smart_report_writer.demos.simple_llm
python -m smart_report_writer.demos.prompt_summary
python -m smart_report_writer.demos.streaming_demo
python -m smart_report_writer.demos.structured_extraction
python -m smart_report_writer.demos.tool_routing_demo
```

