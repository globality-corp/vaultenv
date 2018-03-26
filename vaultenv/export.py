"""
Export variables.

"""
from jinja2 import Environment


def export(variables, template_string, matcher=None):
    """
    Convert variable names using a Jinja2 template string and a regular expression matcher.

    :param variables: a dictionary of variables
    :param template_string: a Jinja2 template string
    :param matcher: a (compiled) regular expression

    """
    template = Environment().from_string(template_string)

    return {
        template.render(key=key): value
        for key, value in variables.items()
        if matcher is None or matcher.match(key)
    }
