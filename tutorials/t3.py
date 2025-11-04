#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
streaming_demo.py — Minimal streaming output with LangChain + Ollama

What this script demonstrates:
- How to enable streaming from an Ollama-backed chat model using LangChain.
- How to iterate over partial chunks (tokens/segments) as they are generated.
- How to print chunks in real time for a responsive CLI experience.

Tip:
- Streaming is great for long answers or when you want immediate feedback in the terminal.
"""

import sys
from langchain_ollama import ChatOllama

def main():
    # ------------------------------------------------------------
    # 1) Initialize the local model with streaming enabled
    # ------------------------------------------------------------
    # - model: any model you've pulled with `ollama pull <model>`.
    # - temperature: higher values yield more varied phrasing.
    # - streaming=True enables incremental generation.
    llm = ChatOllama(
        model="qwen2.5-coder:1.5b",
        temperature=0.3,
        streaming=True
    )

    # ------------------------------------------------------------
    # 2) Define the prompt to generate
    # ------------------------------------------------------------
    prompt = "Generate a concise checklist for taking embedded firmware to production."

    # ------------------------------------------------------------
    # 3) Stream the response
    # ------------------------------------------------------------
    # The .stream(...) method returns an iterator of chunks as they arrive.
    # Each chunk is a LangChain Message-like object with a `.content` string.
    print("\n=== Streaming Output ===\n")
    try:
        for chunk in llm.stream(prompt):
            # Print each incremental piece without a newline to simulate live typing
            print(chunk.content, end="", flush=True)
        print()  # final newline for clean formatting
    except Exception as e:
        print(f"\n[error] Streaming failed: {e}", file=sys.stderr)
        # Optional fallback (non-streaming):
        # resp = llm.invoke(prompt)
        # print("\n[Fallback]\n" + resp.content)

if __name__ == "__main__":
    main()

