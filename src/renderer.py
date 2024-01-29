import jinja2
import yaml


class Renderer:
    MAX_ITERATIONS = 99

    def __init__(self, vars):
        self.vars = vars
        self._render_vars()

    def render(self, template_str):
        rendered_str = jinja2.Template(template_str).render(self.vars)
        return yaml.safe_load(rendered_str)

    def _render_vars(self):
        for _ in range(self.MAX_ITERATIONS):
            rendered_vars = self._deep_render_vars()
            if rendered_vars == self.vars:
                break
            self.vars = rendered_vars
        else:
            raise RuntimeError("Too many iterations. Circular reference?")

    def _deep_render_vars(self, obj=None):
        if obj is None:
            obj = self.vars

        if isinstance(obj, dict):
            return {key: self._deep_render_vars(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._deep_render_vars(item) for item in obj]
        elif isinstance(obj, str) and self._has_jinja(obj):
            return jinja2.Template(obj).render(self.vars)
        else:
            return obj

    @staticmethod
    def _has_jinja(s):
        delimiters = ["{{", "}}", "{%", "%}", "{#", "#}"]
        return any(d in s for d in delimiters)
