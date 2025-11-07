from __future__ import annotations
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import BaseOutputParser

def make_llm(model: str, base_url: str, temperature: float, streaming: bool = False) -> ChatOllama:
    return ChatOllama(model=model, base_url=base_url, temperature=temperature, streaming=streaming)

def chain(prompt, llm: ChatOllama, parser: Optional[BaseOutputParser] = None) -> Runnable:
    runnable = prompt | llm
    if parser is not None:
        runnable = runnable | parser
    return runnable

def stream_in_terminal(runnable: Runnable, inputs: dict) -> str:
    # Stream chunks and also collect the final text
    text = []
    for chunk in runnable.stream(inputs):
        # `chunk` is a Message-like object with `.content`
        piece = getattr(chunk, "content", str(chunk))
        print(piece, end="", flush=True)
        text.append(piece)
    print()
    return "".join(text)
