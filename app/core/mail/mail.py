import os

from jinja2 import Environment, FileSystemLoader
import html2text


def render_template(template_name: str, **kwargs) -> tuple[str, str]:
    """
    Returns the rendered content of a mail template as html and text.
    The template name has no extension or location. Example: "welcome"
    Intended for use with mailman.EmailMultiAlternatives()
    """

    env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/templates'))
    template = env.get_template(template_name + '.html')
    html = template.render(**kwargs)

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True # Ignore converting links from html to text
    text = text_maker.handle(html)

    return html, text
