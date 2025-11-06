# 🧠 LangChain + Ollama Mini Tutorials

This repository contains a collection of **tiny, fully working examples** showing how to use
[LangChain](https://python.langchain.com/) with [Ollama](https://ollama.com/) for local LLM workflows —
from simple prompts to streaming, structured outputs, and RAG indexing.

Each example is **stand-alone**: run it directly with `make run I=<tutorial_number>.py`.

---

## 📦 Requirements

Install dependencies once:

```bash
pip install -r requirements.txt
```

Install and run **Ollama** in the background (see the official site for your OS).

Pull at least one model to use in the tutorials:

```bash
ollama pull qwen2.5-coder:1.5b
ollama pull qwen3-embedding:0.6b
```

List locally available models:

```bash
ollama list
```

> Tip: You can swap any model name used in these scripts with another one you've pulled.

---

## 🧩 Tutorials Overview

| File | What it demonstrates |
|------|-----------------------|
| **`t1.py`** | The “Hello World” — send a single prompt to a local Ollama model and print the response. |
| **`t2.py`** | Build a structured `ChatPromptTemplate` (system + user) with a `{topic}` variable. |
| **`t3.py`** | **Streaming** output: print tokens/chunks as the LLM generates them (great for CLIs). |
| **`t4.py`** | **Structured output parsing**: force JSON that matches a `Pydantic` schema (e.g., a `Part`). |
| **`t5.py`** | One-file **RAG** with LangChain + Chroma + Ollama: auto-download a tiny corpus, index, and answer a preset question. |
| **`t6.py`** | **Tool selection via structured output**: the model emits an `Action` choosing `math`/`weather`/`none`. |

---

## 🚀 Quick Start

Clone or copy the files into a folder, then:

```bash
# 1) Install Python deps
pip install -r requirements.txt

# 2) Pull at least one model
ollama pull qwen2.5-coder:1.5b
ollama pull mistral:7b-instruct

# 3) Run any tutorial
python simple_llm.py
```

---

## 📜 Usage Details

### 1) `t1.py`
Minimal example using `ChatOllama` to send one prompt and print the reply.

```bash
make run I=1
```

**Customize:** edit the prompt string or set a different `model=` in the script.

---

### 2) `t2.py`
Shows prompt templating with `ChatPromptTemplate` + chain piping (`prompt | llm`).

```bash
make run I=2
```

Environment overrides (optional):

```bash
TOPIC="USB-C Power Delivery" BULLETS=7 MODEL="mistral:7b-instruct" TEMP=0.2 python prompt_summary.py
```

---

### 3) `t3.py`
Streams response chunks in real-time using `llm.stream(...)`.

```bash
python streaming_demo.py
make run I=3
```

**Tip:** perfect for long answers where you want immediate feedback in the terminal.

---

### 4) `structured_extraction.py`
Forces the model to return JSON matching a Pydantic schema and parses it safely.

```bash
make run I=4
```

**Edit the schema** in the file (`class Part(...)`) to fit your own data model.

---

### 5) `t5.py` (RAG one-file)
One-file RAG: downloads a few HTTP RFCs as `.txt`, builds/loads a persistent **Chroma** index, retrieves, and answers a fixed question.

```bash
make run I=5
```

Optional environment variable to change the question without editing the file:

```bash
Q="Explain HTTP ETags and If-None-Match" python t5.py
```

**Customize corpus:** replace the URLs in `URLS` with other `.txt` sources.

---

### 6) `t6.py`
The model picks a tool (`math`, `weather`, or `none`) and provides an argument.
The script parses the decision (`Action`) and dispatches to the chosen tool.

```bash
make run I=6
```

- Uses a **safe math evaluator** (AST-based) instead of raw `eval`.
- Weather is a stub to keep the example self-contained.

---

## 🔧 Troubleshooting

- **Ollama connection error**  
  Make sure the Ollama service is running and that you’ve pulled the model used in the script.  
  Try: `ollama list` and `ollama pull <model>`.

- **Model too large / runs out of memory**  
  Choose a smaller model (e.g., `qwen2.5-coder:1.5b`) or reduce context sizes / chunk counts.

- **UnicodeDecodeError when loading files** (`t5.py`)  
  The loader uses UTF-8; for other encodings, convert your corpus to UTF-8 or replace the loader.

- **Slow first run**  
  Building an index or loading a model the first time can take longer. Subsequent runs are faster (thanks to Chroma persistence and local model caching).

---

## 🧪 Model Swaps

All scripts default to lightweight models you can run locally. You can replace them with any model you’ve pulled in Ollama, such as:

- `mistral:7b-instruct`
- `qwen2.5:latest`
- `llama3.1:8b`

Just change the `model=` parameter or set `MODEL=...` where supported.

---

## 📄 License

These examples are provided for educational purposes. Use them freely in your own projects.

