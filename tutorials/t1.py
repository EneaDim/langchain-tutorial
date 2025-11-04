#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
simple_llm.py — Minimal example using LangChain + Ollama

This script:
1. Initializes a local LLM served by Ollama via LangChain.
2. Sends a simple natural-language prompt to the model.
3. Prints the model’s response.

It’s the smallest possible LangChain-Ollama demo for local chat models.
"""

# Import the LangChain wrapper for Ollama’s local chat models.
# This class lets you send text prompts and get structured responses easily.
from langchain_ollama import ChatOllama


# ------------------------------------------------------------
# 1) Initialize the local model
# ------------------------------------------------------------
# - model: name of an Ollama model you’ve pulled, e.g. “qwen2.5-coder:1.5b”.
#   You can check available models with `ollama list` and pull new ones with `ollama pull <model>`.
# - temperature: controls randomness. 0.0 = deterministic, >0 = more creative.
#
# NOTE: Ollama must be running locally (the Ollama service automatically starts in the background).
llm = ChatOllama(
    model="qwen2.5-coder:1.5b",  # any valid Ollama model name
    temperature=0.2              # slight randomness for variety in phrasing
)


# ------------------------------------------------------------
# 2) Send a prompt to the model
# ------------------------------------------------------------
# You can send any string prompt to .invoke() — it’s synchronous and simple.
# This one asks for a short, structured answer (“3 bullet points”).
response = llm.invoke("Explain in 3 points the difference between an MCU and an MPU.")


# ------------------------------------------------------------
# 3) Print the model’s output
# ------------------------------------------------------------
# The ChatOllama object returns a LangChain Message object with `.content` containing the text.
print(response.content)

