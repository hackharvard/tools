from jinja2 import Environment, StrictUndefined

JINJA = Environment(undefined=StrictUndefined, autoescape=False)

def render_fields(data: dict, context: dict) -> dict:
    """Renders all string fields in `data` as Jinja2 templates using `context`."""
    out = dict(data)
    for key, val in data.items():
        if isinstance(val, str):
            out[key] = JINJA.from_string(val).render(**context)

    return out