from jinja2 import Template
import yaml


def render_chat(template_str, data):
    template = Template(template_str)
    rendered_template = template.render(data)
    return yaml.safe_load(rendered_template)
