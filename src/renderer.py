import jinja2
import yaml


def render(template_str, vars):
    for _ in range(10):
        rendered_vars = _deep_render_vars(vars)
        if rendered_vars == vars:
            break
        vars = rendered_vars
    else:
        raise RuntimeError("Too many iterations")
    rendered_template = jinja2.Template(template_str).render(vars)
    return yaml.safe_load(rendered_template)


def _deep_render_vars(vars, obj=None):
    if obj is None:
        obj = vars

    if isinstance(obj, dict):
        return {key: _deep_render_vars(vars, value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_deep_render_vars(vars, item) for item in obj]
    elif isinstance(obj, str):
        return jinja2.Template(obj).render(vars)
    else:
        raise ValueError(f"Unknown type: {type(obj)}")
