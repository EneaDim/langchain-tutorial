#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
prompt_summary.py — Minimal prompt templating with LangChain + Ollama

What this does:
1) Builds a small chat prompt template with a {topic} variable.
2) Pipes (|) the prompt into an Ollama-backed chat model to form a runnable chain.
3) Invokes the chain with a specific topic and prints the model's response.

Customize via environment variables (optional):
  TOPIC="USB-C Power Delivery" python prompt_summary.py
  BULLETS=7 python prompt_summary.py
  MODEL="mistral:7b-instruct" python prompt_summary.py
  TEMP=0.0 python prompt_summary.py
"""

import os
import sys

# LangChain wrapper for local Ollama chat models
from langchain_ollama import ChatOllama

# Prompt builder: lets you compose chat-style prompts with variables
from langchain_core.prompts import ChatPromptTemplate


# =========================
# Configuration (editable)
# =========================

# Topic to summarize; can be overridden with env var TOPIC
TOPIC = os.environ.get("TOPIC", "USB-C Power Delivery")

# Number of bullet points to request in the summary
BULLETS = int(os.environ.get("BULLETS", "5"))

# Ollama model to use (make sure it's installed: `ollama pull <model>`)
MODEL = os.environ.get("MODEL", "qwen2.5-coder:1.5b")

# Sampling temperature (0.0 = deterministic)
TEMP = float(os.environ.get("TEMP", "0.0"))


def main():
    # ------------------------------------------------------------
    # 1) Define a chat prompt template
    # ------------------------------------------------------------
    # - "system" message sets assistant behavior: concise + technical.
    # - "user" message has a {topic} variable we will fill at runtime.
    #   We also inject the desired number of bullets via f-string.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a very concise technical assistant."),
        ("user", f"Summarize in {BULLETS} bullet points: {{topic}}"),
    ])

    # ------------------------------------------------------------
    # 2) Initialize the local chat model via Ollama
    # ------------------------------------------------------------
    # If you see a connection error:
    #   - Ensure the Ollama service is running
    #   - Ensure the model exists: `ollama pull {MODEL}`
    llm = ChatOllama(model=MODEL, temperature=TEMP)

    # ------------------------------------------------------------
    # 3) Compose a chain: prompt → llm
    # ------------------------------------------------------------
    # The pipe operator (|) builds a runnable:
    #   - Formats the prompt with variables
    #   - Sends it to the model
    #   - Returns a message object with `.content`
    chain = prompt | llm

    # ------------------------------------------------------------
    # 4) Invoke the chain and print the result
    # ------------------------------------------------------------
    print(f"[topic] {TOPIC}\n")
    try:
        response = chain.invoke({"topic": TOPIC})
        print("=== ANSWER ===\n")
        print(response.content)
    except Exception as e:
        print(f"Error while invoking the chain: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
