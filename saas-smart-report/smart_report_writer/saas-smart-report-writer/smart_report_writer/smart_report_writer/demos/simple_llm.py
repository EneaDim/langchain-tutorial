#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain_ollama import ChatOllama

def main():
    llm = ChatOllama(model="qwen2.5-coder:1.5b", temperature=0.2)
    resp = llm.invoke("Explain in 3 points the difference between an MCU and an MPU.")
    print(resp.content)

if __name__ == "__main__":
    main()
