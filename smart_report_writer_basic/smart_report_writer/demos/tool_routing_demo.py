#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import ast, operator as op

class Action(BaseModel):
    tool: str = Field(description="one of: weather, math, none")
    argument: str

_ALLOWED_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv, ast.Mod: op.mod, ast.Pow: op.pow,
    ast.USub: op.neg, ast.UAdd: op.pos,
}

def _eval_node(node: ast.AST):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        fn = _ALLOWED_OPS.get(type(node.op))
        if fn is None: raise ValueError("Operator not allowed")
        return fn(left, right)
    if isinstance(node, ast.UnaryOp):
        fn = _ALLOWED_OPS.get(type(node.op))
        if fn is None: raise ValueError("Operator not allowed")
        return fn(_eval_node(node.operand))
    raise ValueError(f"Unsupported node: {type(node).__name__}")

def safe_eval(expr: str) -> str:
    try:
        tree = ast.parse(expr, mode="eval")
        return str(_eval_node(tree.body))
    except Exception as e:
        return f"[math error] {e}"

def tool_math(x: str) -> str:
    return safe_eval(x)

def tool_weather(x: str) -> str:
    city = x.strip() or "Unknown"
    return f"Weather (fake) for {city}: clear skies, light breeze."

TOOLS = {"math": tool_math, "weather": tool_weather}

def main():
    parser = PydanticOutputParser(pydantic_object=Action)
    fmt = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(
        "Se devi calcolare usa tool=math con l'espressione.\n"
        "Se chiedono meteo, usa tool=weather con la città.\n"
        "Altrimenti tool=none.\n"
        "{fmt}\n"
        "Input: {q}"
    )
    llm = ChatOllama(model="qwen2.5-coder:1.5b", temperature=0.0)
    messages = prompt.format_messages(fmt=fmt, q="Quanto fa (12+7)*3?")
    response = llm.invoke(messages)
    raw_text = response.content
    try:
        act: Action = parser.parse(raw_text)
    except Exception as e:
        print("[parser error] Could not parse model output.")
        print("Raw response:\n", raw_text)
        print("Error:", e)
        return
    chosen_tool = act.tool.strip().lower()
    argument = act.argument.strip()
    if chosen_tool in TOOLS:
        result = TOOLS[chosen_tool](argument)
        print("TOOL:", chosen_tool)
        print("ARG :", argument)
        print("RESULT:", result)
    else:
        print("LLM RESPONSE:", argument)

if __name__ == "__main__":
    main()
