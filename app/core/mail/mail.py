import os

from jinja2 import Environment, FileSystemLoader
import html2text


def create_html_and_txt_from_template(template_name: str, **kwargs) -> tuple[str, str]:
    """ Returns the content of a template as html and text """

    env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/templates'))
    template = env.get_template(template_name + '.html')
    html = template.render(**kwargs)

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True # Ignore converting links from html to text
    text = text_maker.handle(html)

    return html, text
