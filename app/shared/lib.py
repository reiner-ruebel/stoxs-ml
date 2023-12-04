import os
import re

def module_name_to_url_prefix(module_name: str) -> tuple[str, str]:
    """ Converts a module name like app.auth.register to the default name ('register') and url_prefix ('/app/auth') of a flask blueprint """

    segments = module_name.split('.')
    name = segments[-1]
    url_prefix = '/' + '/'.join(segments)
    
    return (name, url_prefix)


def valid_mail_address(mail_address: str) -> bool:
    """ Checks if a mail address is valid """
    return True if re.match(r"[^@]+@[^@]+\.[^@]+", mail_address) else False


def get_module_names(folder: str) -> list[str]:
    """ Creates a list of module names without the extension within a folder """
    return [module[:-3] for module in os.listdir(folder) if module.endswith('.py') and module != '__init__.py']


def get_application_path() -> str:
    """ Returns the root path of the application """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
