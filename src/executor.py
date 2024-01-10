from jinja2 import Template
import yaml
import openai


def _render(template_str, vars, context):
    template = Template(template_str)
    rendered_template = template.render(vars=vars, context=context)
    return yaml.safe_load(rendered_template)


def _complete(messages):
    return (
        openai.OpenAI()
        .chat.completions.create(
            messages=messages,
            model="gpt-4-vision-preview",
        )
        .choices[0]
        .message.content
    )


def execute(template_str, vars, context, update_func):
    rendered_template = _render(template_str, vars, context)
    response = _complete(rendered_template)
    return update_func(context, response)
