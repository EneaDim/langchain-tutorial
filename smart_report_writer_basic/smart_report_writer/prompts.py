from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

DOC_SUMMARY_PROMPT = PromptTemplate.from_template(
    """You are a senior business analyst producing a client-facing summary.
Rules: no hallucinations; no repetition; group similar items; omit empty sections.
Format:
# Executive Summary
## Overview
## Decisions & Rationale
## Open Questions
## Constraints
## Next Steps
Use bullets: '-', '  -', '    -'. Keep bullets concise, measurable.
Content:
{content}""")

LOGCFG_SUMMARY_PROMPT = PromptTemplate.from_template(
    """You are an ops engineer summarizing logs/configs for execs.
Show patterns, risks, concrete fixes; quantify counts/time. Collapse duplicates with (×N).
Sections (omit empty): ## Issues Observed ## Patterns ## Likely Root Causes ## Immediate Fixes ## Follow-up Experiments
Bullets '-', '  -'. Input:
{content}""")

CODE_SUMMARY_PROMPT = PromptTemplate.from_template(
    """You are a staff engineer writing a business-readable code overview.
Extract: architecture, interfaces, flags, risks, observability. No invention. Merge duplicates.
Sections (omit empty): ## Architecture Overview ## Components & Interfaces ## Risks ## Suggestions
Bullets '-', '  -'. Input:
{content}""")

TABLE_SUMMARY_PROMPT = PromptTemplate.from_template(
    """You are a data analyst writing 5–7 concise bullets.
Use one line per bullet; add a sub-bullet with evidence if useful; avoid restating schema; note multiplicity (×N).
Input JSON:
{profile_json}""")

MASTER_SYNTH_PROMPT = PromptTemplate.from_template(
    """You are a principal analyst producing a board-ready synthesis.
Hard rules: no duplication; no hallucination; bullets < 20 words; measurable when possible.
Output:
# Executive Summary
## Key Findings
## Risks & Gaps
## Recommendations (Next 30–60 days)
## Appendix
Inputs:
Manifest JSON:
{manifest_json}
Per-type Summaries (Markdown):
{per_type_summaries}""")
