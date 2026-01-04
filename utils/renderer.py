from jinja2 import Template
from utils.templates import TEMPLATES
import textwrap

def render_report_from_template(report_type: str, context: dict) -> str:
    template_str = TEMPLATES.get(report_type)
    if not template_str:
        raise ValueError(f"Unsupported report type: {report_type}")
    tpl = Template(textwrap.dedent(template_str))
    report_prompt = tpl.render(**context)

    return (
        "You are a concise, professional analyst. Write the following report in Markdown only.\n\n"
        + report_prompt
    )
