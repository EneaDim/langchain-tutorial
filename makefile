# ---------- Config ----------
PY             ?= python3
VENV_DIR       ?= .venv
PIP            := $(VENV_DIR)/bin/pip
PYTHON         := $(VENV_DIR)/bin/python
ACTIVATE       := source $(VENV_DIR)/bin/activate
REQUIREMENTS   ?= requirements.txt

# Tutorial selection: make run I=3 -> esegue tutorials/tut3.py
I              ?= 1
TUT_DIR        ?= tutorials
TUT_PATTERN    ?= t$(I).py
TUT_FILE       := $(TUT_DIR)/$(TUT_PATTERN)

# Modelli Ollama da scaricare (personalizzabili da CLI: make pull MODELS="mistral:7b-instruct qwen2.5:7b-instruct")
MODELS         ?= codellama:7b-instruct qwen2.5-coder:1.5b
OLLAMA_LOG_DIR ?= logs
OLLAMA_LOG     := $(OLLAMA_LOG_DIR)/ollama.log
OLLAMA_PID     := .ollama.pid

# ---------- Help ----------
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Target principali:"
	@echo "  make setup             # crea venv e installa dipendenze"
	@echo "  make pull              # ollama pull dei modelli (variabile MODELS=...)"
	@echo "  make start-ollama      # avvia 'ollama serve' in background"
	@echo "  make run I=3           # esegue l'i-esimo tutorial (tutorials/tut3.py)"
	@echo "  make list              # mostra i tutorial disponibili"
	@echo "  make stop-ollama       # ferma 'ollama serve' avviato da questo Makefile"
	@echo "  make clean             # pulizia venv, pid e cache"

# ---------- Env / Deps ----------
$(VENV_DIR):
	@$(PY) -m venv $(VENV_DIR)
	@echo "[venv] Creato $(VENV_DIR)"

$(REQUIREMENTS):
	@echo "langchain"                          >  $(REQUIREMENTS)
	@echo "langchain-ollama"                  >> $(REQUIREMENTS)
	@echo "langchain-community"               >> $(REQUIREMENTS)
	@echo "langchain-text-splitters"          >> $(REQUIREMENTS)
	@echo "chromadb"                          >> $(REQUIREMENTS)
	@echo "pydantic"                          >> $(REQUIREMENTS)
	@echo "python-dotenv"                     >> $(REQUIREMENTS)
	@echo "pymupdf"                           >> $(REQUIREMENTS)  # utile per PDF (opzionale)
	@echo "[req] Scritto $(REQUIREMENTS)"

.PHONY: setup
setup: $(VENV_DIR) $(REQUIREMENTS)
	@$(PIP) install --upgrade pip >/dev/null
	@$(PIP) install -r $(REQUIREMENTS)
	@echo "[setup] Dipendenze installate."

# ---------- Ollama ----------
.PHONY: pull
pull:
	@command -v ollama >/dev/null 2>&1 || { echo "Errore: 'ollama' non trovato nel PATH."; exit 1; }
	@for m in $(MODELS); do \
		echo "[ollama] pull $$m"; \
		ollama pull $$m || exit 1; \
	done
	@echo "[ollama] Modelli pronti."

$(OLLAMA_LOG_DIR):
	@mkdir -p $(OLLAMA_LOG_DIR)

.PHONY: start-ollama
start-ollama: $(OLLAMA_LOG_DIR)
	@command -v ollama >/dev/null 2>&1 || { echo "Errore: 'ollama' non trovato nel PATH."; exit 1; }
	@if pgrep -x "ollama" >/dev/null; then \
		echo "[ollama] già in esecuzione."; \
	else \
		echo "[ollama] avvio in background... (log: $(OLLAMA_LOG))"; \
		nohup ollama serve > $(OLLAMA_LOG) 2>&1 & echo $$! > $(OLLAMA_PID); \
		sleep 1; \
		if pgrep -x "ollama" >/devnull; then echo "[ollama] avviato."; fi; \
	fi

.PHONY: stop-ollama
stop-ollama:
	@if [ -f "$(OLLAMA_PID)" ]; then \
		kill `cat $(OLLAMA_PID)` || true; \
		rm -f $(OLLAMA_PID); \
		echo "[ollama] fermato (via PID file)."; \
	else \
		# fallback: prova a killare processo 'ollama serve' se esiste
		pkill -x ollama || true; \
		echo "[ollama] fermato (best-effort)."; \
	fi

# ---------- Run tutorials ----------
.PHONY: list
list:
	@echo "Tutorial disponibili in $(TUT_DIR):"
	@ls -1 $(TUT_DIR)/*.py 2>/dev/null || echo "(nessun file trovato)"

.PHONY: run
run: start-ollama
	@test -f "$(TUT_FILE)" || { echo "File non trovato: $(TUT_FILE)"; exit 2; }
	@echo "[run] Eseguo $(TUT_FILE)"
	@$(PYTHON) "$(TUT_FILE)"

# ---------- Utilities ----------
.PHONY: clean
clean:
	@rm -rf $(VENV_DIR) __pycache__ .pytest_cache .mypy_cache .ruff_cache
	@rm -f  $(OLLAMA_PID)
	@echo "[clean] Pulizia base completata."
