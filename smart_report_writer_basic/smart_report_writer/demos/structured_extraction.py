#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field, ValidationError
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser

class Part(BaseModel):
    name: str
    unit_price: float = Field(ge=0, description="Unit price in EUR")
    stock: int = Field(ge=0, description="Available quantity")

parser = PydanticOutputParser(pydantic_object=Part)
format_instructions = parser.get_format_instructions()
prompt = ChatPromptTemplate.from_template(
    "Return the answer using the required format only.\n"
    "{fmt}\n"
    "Input: {q}"
)
RAW_INPUT = "Resistenza 10k 1% 0603, 0.02€, stock 2500"
MODEL_NAME = "qwen2.5-coder:1.5b"

def main():
    llm = ChatOllama(model=MODEL_NAME, temperature=0.0)
    messages = prompt.format_messages(fmt=format_instructions, q=RAW_INPUT)
    response = llm.invoke(messages)
    text = response.content
    try:
        obj: Part = parser.parse(text)
    except ValidationError as ve:
        print("Failed to parse model output. Raw response:\n")
        print(text)
        print("\nValidation error:\n", ve)
        return
    print("Parsed Part object:")
    print(obj)
    print("\nFields:")
    print(f"- name      : {obj.name}")
    print(f"- unit_price: {obj.unit_price}")
    print(f"- stock     : {obj.stock}")

if __name__ == "__main__":
    main()
