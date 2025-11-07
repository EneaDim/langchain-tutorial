from jinja2 import Environment, BaseLoader, Template
from smart_report_writer.core.templates.filters import filters

def get_env():
    env = Environment(loader=BaseLoader(), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    for name, fn in filters().items():
        env.filters[name] = fn
    return env

def render(template_str: str, context: dict) -> str:
    env = get_env()
    return env.from_string(template_str).render(**context)
