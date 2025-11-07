from __future__ import annotations
from typing import Dict, Any, List
import json
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_core.output_parsers import StrOutputParser
from ..llm import chain as make_chain
from ..prompts import (
    DOC_SUMMARY_PROMPT, LOGCFG_SUMMARY_PROMPT, CODE_SUMMARY_PROMPT,
    TABLE_SUMMARY_PROMPT, MASTER_SYNTH_PROMPT
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
async def arun(runnable, **kw):
    return await runnable.ainvoke(kw)

def category_runnable(llm, prompt):
    return make_chain(prompt, llm, StrOutputParser())

def tables_runnable(llm):
    # returns a function that runs per-profile
    return make_chain(TABLE_SUMMARY_PROMPT, llm, StrOutputParser())

def master_runnable(llm):
    return make_chain(MASTER_SYNTH_PROMPT, llm, StrOutputParser())
