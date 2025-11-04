#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tool_routing_demo.py — Tool selection with Pydantic parsing + LangChain + Ollama

What this script demonstrates:
- Define a strict output schema (`Action`) with Pydantic.
- Ask an LLM to decide which "tool" to call (math / weather / none) and with what argument.
- Parse the model's response into a validated `Action`.
- Dispatch to the selected tool and print the final result.

Notes:
- Prompts are in Italian (to mirror your original example); code comments are in English.
- The math tool uses a SAFE arithmetic evaluator (AST-based), not Python's raw eval.
"""

from typing import Any
from pydantic import BaseModel, Field, ValidationError

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

import ast
import operator as op


# ===========================
# 1) Define the Action schema
# ===========================
class Action(BaseModel):
    """Structured decision emitted by the LLM."""
    tool: str = Field(description="one of: weather, math, none")
    argument: str


# ======================================
# 2) A safe arithmetic evaluator for math
# ======================================
# Allowed operators for simple arithmetic:
_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _eval_node(node: ast.AST) -> Any:
    """Recursively evaluate a limited set of AST nodes safely."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # numbers only
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed.")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed.")
        return _ALLOWED_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed.")
        return _ALLOWED_OPS[op_type](operand)
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    if isinstance(node, ast.Paren := getattr(ast, "Tuple", object)):  # placeholder; we don't actually allow tuples
        raise ValueError("Tuples are not allowed.")
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")

def safe_eval(expr: str) -> str:
    """
    Safely evaluate a basic arithmetic expression using Python's AST.
    Supported: +, -, *, /, //, %, **, parentheses, numeric literals.
    Returns a string for uniform printing.
    """
    try:
        # Parse in 'eval' mode to restrict to a single expression
        tree = ast.parse(expr, mode="eval")
        result = _eval_node(tree.body)
        return str(result)
    except Exception as e:
        return f"[math error] {e}"


# ============================================
# 3) Tool registry (functions the LLM can call)
# ============================================
def tool_math(x: str) -> str:
    """Math tool using safe_eval to avoid arbitrary code execution."""
    return safe_eval(x)

def tool_weather(x: str) -> str:
    """Toy weather tool that fabricates a brief forecast."""
    city = x.strip() or "Unknown"
    return f"Weather (fake) for {city}: clear skies, light breeze."

TOOLS = {
    "math": tool_math,
    "weather": tool_weather,
}


# =========================================================
# 4) Build the parser, format instructions, and the prompt
# =========================================================
parser = PydanticOutputParser(pydantic_object=Action)
fmt = parser.get_format_instructions()

# Prompt in Italian (as in your example). It instructs the model how to choose a tool.
prompt = ChatPromptTemplate.from_template(
    "Se devi calcolare usa tool=math con l'espressione.\n"
    "Se chiedono meteo, usa tool=weather con la città.\n"
    "Altrimenti tool=none.\n"
    "{fmt}\n"
    "Input: {q}"
)


# ============================
# 5) Initialize the local LLM
# ============================
llm = ChatOllama(model="qwen2.5-coder:1.5b", temperature=0.0)


# ============================
# 6) Run a test query end-to-end
# ============================
def main():
    # Example input asking for a calculation
    user_input = "Quanto fa (12+7)*3?"

    # Format messages with the format instructions and user input
    messages = prompt.format_messages(fmt=fmt, q=user_input)

    # Call the model and parse into our structured Action
    response = llm.invoke(messages)
    raw_text = response.content

    try:
        act: Action = parser.parse(raw_text)
    except Exception as e:
        print("[parser error] Could not parse model output.")
        print("Raw response:\n", raw_text)
        print("Error:", e)
        return

    # Route to the selected tool if available; otherwise, treat as plain LLM output
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

