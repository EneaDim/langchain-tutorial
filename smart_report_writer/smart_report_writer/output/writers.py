from __future__ import annotations
import os
from jinja2 import Environment, FileSystemLoader, BaseLoader

def write_with_template(jinja_env, template_name: str, context: dict, path: str) -> str:
    tpl = jinja_env.get_template(template_name)
    text = tpl.render(**context)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

def ensure_env(templates_dir: str | None):
    if templates_dir:
        return Environment(loader=FileSystemLoader(templates_dir), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    return Environment(loader=BaseLoader(), autoescape=False, trim_blocks=True, lstrip_blocks=True)
