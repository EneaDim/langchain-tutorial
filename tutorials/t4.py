#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
structured_extraction.py — Structured outputs with LangChain + Pydantic + Ollama

What this script demonstrates:
- Defining a strict data schema with Pydantic (Part).
- Asking an LLM to return data in that schema using LangChain's PydanticOutputParser.
- Parsing the LLM response into a validated Python object (with numeric constraints).
- Defensive error handling for malformed outputs.

How it works:
1) We create a Pydantic model `Part` describing the expected fields and constraints.
2) We instantiate `PydanticOutputParser` with that model — it knows how to:
   - produce format instructions for the LLM,
   - parse the model's text response back into a `Part` instance.
3) We build a prompt that includes those format instructions + a natural-language input.
4) We pass the prompt to an Ollama-backed chat model.
5) We parse and print the resulting object.

Customize:
- Change the `RAW_INPUT` string to extract a different component.
- Swap `MODEL_NAME` with any model you’ve pulled in Ollama.
"""

from pydantic import BaseModel, Field, ValidationError
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser

# ======================
# 1) Define the schema
# ======================

class Part(BaseModel):
    """
    A simple, structured representation of an electronic part.
    - name: human-readable name or designation (e.g., "Resistor 10k 1% 0603")
    - unit_price: price per unit (must be >= 0)
    - stock: on-hand inventory count (must be >= 0)
    """
    name: str
    unit_price: float = Field(ge=0, description="Unit price in EUR")
    stock: int = Field(ge=0, description="Available quantity")

# The parser encodes/decodes between text and the Pydantic model
parser = PydanticOutputParser(pydantic_object=Part)

# Generate precise formatting instructions (e.g., JSON schema the model should follow)
format_instructions = parser.get_format_instructions()

# ======================
# 2) Build the prompt
# ======================
# We keep the prompt simple: instruct to follow the required format, then provide the input.
prompt = ChatPromptTemplate.from_template(
    "Return the answer using the required format only.\n"
    "{fmt}\n"
    "Input: {q}"
)

# Example raw input in natural language (Italian here, but any language is fine)
RAW_INPUT = "Resistenza 10k 1% 0603, 0.02€, stock 2500"

# ======================
# 3) Initialize the LLM
# ======================
MODEL_NAME = "qwen2.5-coder:1.5b"  # ensure you've pulled it: `ollama pull qwen2.5-coder:1.5b`
llm = ChatOllama(model=MODEL_NAME, temperature=0.0)

def main():
    # Format the chat messages with our instructions + input
    messages = prompt.format_messages(fmt=format_instructions, q=RAW_INPUT)

    # Call the model synchronously
    response = llm.invoke(messages)

    # The model should return a string that matches the format_instructions (often JSON)
    text = response.content

    # Try to parse into a validated Pydantic object
    try:
        obj: Part = parser.parse(text)
    except ValidationError as ve:
        # If the model didn't follow the schema strictly, show the raw text and error
        print("Failed to parse model output. Raw response:\n")
        print(text)
        print("\nValidation error:\n", ve)
        return

    # Success — print the object and its fields
    print("Parsed Part object:")
    print(obj)  # pretty __repr__ from Pydantic
    print("\nFields:")
    print(f"- name      : {obj.name}")
    print(f"- unit_price: {obj.unit_price}")
    print(f"- stock     : {obj.stock}")

if __name__ == "__main__":
    main()

