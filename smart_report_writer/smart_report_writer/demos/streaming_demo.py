#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from langchain_ollama import ChatOllama

def main():
    llm = ChatOllama(model="qwen2.5-coder:1.5b", temperature=0.3, streaming=True)
    prompt = "Generate a concise checklist for taking embedded firmware to production."
    print("\n=== Streaming Output ===\n")
    try:
        for chunk in llm.stream(prompt):
            print(chunk.content, end="", flush=True)
        print()
    except Exception as e:
        print(f"\n[error] Streaming failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
