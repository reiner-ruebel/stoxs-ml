import os
import re

from jinja2 import Environment, FileSystemLoader
from html2text import HTML2Text


class Mail:
    @staticmethod
    def render_template(template_name: str, **kwargs) -> tuple[str, str]:
        """
        Returns the rendered content of a mail template as html and text.
        The template name has no extension or location. Example: "welcome"
        Intended for use with mailman.EmailMultiAlternatives()
        """

        env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + '/templates'))
        template = env.get_template(template_name + '.html')
        html = template.render(**kwargs)

        text_maker = HTML2Text()
        text_maker.ignore_links = True # Ignore converting links from html to text
        text = text_maker.handle(html)

        return html, text
    

    @staticmethod
    def valid_email_address(email_address: str) -> bool:
        """ Checks if an email address is valid. """
        return True if re.match(r"[^@]+@[^@]+\.[^@]+", email_address) else False
