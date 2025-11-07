# Simple Makefile: setup, help, run
# Usage:
#   make setup
#   make run INPUTS="docs/**/*" TOPIC="Smart Coffee"
#   make run-docx INPUTS="docs/**/*" TOPIC="Smart Coffee" DOCX_TEMPLATE="templates/business_report.docx"

VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
SCRIPT      ?= smart_report_writer.cli

# Defaults (override from CLI if needed)
INPUTS      ?= bench/**/*
RECURSIVE   ?= --recursive
TOPIC       ?= Smart Coffee
MODEL       ?= llama3.2
BASE_URL    ?= http://localhost:11434
TEMP        ?= 0.2
SUMMARY_OUT ?= summary.md
DETAILED_OUT?= report.md
DOCX_TEMPLATE ?=

.PHONY: help setup run run-docx

help:
	@echo "Targets:"
	@echo "  setup        Create .venv and install requirements.txt"
	@echo "  run          Generate summary.md and report.md (Markdown)"
	@echo "  run-docx     Generate summary.md and a DOCX using a template"
	@echo ""
	@echo "Variables (override as needed):"
	@echo "  INPUTS, RECURSIVE, TOPIC, MODEL, BASE_URL, TEMP, SUMMARY_OUT, DETAILED_OUT, DOCX_TEMPLATE"

setup:
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; else echo "No requirements.txt found"; fi
	@echo "✅ Setup done."

run:
	@$(PY) -m $(SCRIPT) \
		-i "$(INPUTS)" $(RECURSIVE) \
		--topic "$(TOPIC)" \
		--summary-out "$(SUMMARY_OUT)" \
		--detailed-out "$(DETAILED_OUT)" \
		--model "$(MODEL)" \
		--base-url "$(BASE_URL)" \
		--temperature $(TEMP)

run-docx:
	@if [ -z "$(DOCX_TEMPLATE)" ]; then echo "❌ Set DOCX_TEMPLATE=path/to/template.docx"; exit 1; fi
	@$(PY) -m $(SCRIPT) \
		-i "$(INPUTS)" $(RECURSIVE) \
		--topic "$(TOPIC)" \
		--summary-out "$(SUMMARY_OUT)" \
		--detailed-out "$(DETAILED_OUT)" \
		--docx-template-file "$(DOCX_TEMPLATE)" \
		--model "$(MODEL)" \
		--base-url "$(BASE_URL)" \
		--temperature $(TEMP)

