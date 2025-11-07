#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

TOPIC = os.environ.get("TOPIC", "USB-C Power Delivery")
BULLETS = int(os.environ.get("BULLETS", "5"))
MODEL = os.environ.get("MODEL", "qwen2.5-coder:1.5b")
TEMP = float(os.environ.get("TEMP", "0.0"))

def main():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a very concise technical assistant."),
        ("user", f"Summarize in {BULLETS} bullet points: {{topic}}"),
    ])
    llm = ChatOllama(model=MODEL, temperature=TEMP)
    chain = prompt | llm
    print(f"[topic] {TOPIC}\n")
    resp = chain.invoke({"topic": TOPIC})
    print("=== ANSWER ===\n")
    print(resp.content)

if __name__ == "__main__":
    main()
