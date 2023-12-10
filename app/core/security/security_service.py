from typing import Optional

from app.core.security.user import User
from app.core.application.config import CustomConfig
from app.shared.utils import valid_mail_address


#
# data retrieval
#

def user_exist(username: str, email: str) -> bool:
    """ Checks if a user with the given username exists. """
    return User.query.filter((User.username == username) | (User.email == email)).count() > 0


def get_user_by_username(username: str) -> Optional[User]:
    """ Returns the user with the given username. """
    return User.query.filter(User.username == username).first()


#
# custom policies
#

def user_policy_checker(password: str, username: str, mail: str) -> Optional[list[str]]:
    """ Checks if the password meets custom requirements. """

    config = CustomConfig()
    errors: list[str] = []
    
    if config.CUSTOM_REQUIRE_DIGITS:
        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit.")

    if config.CUSTOM_REQUIRE_LOWERCASE:
        if not any(char.islower() for char in password):
            errors.append("Password must contain at least one lowercase letter.")
            
    if config.CUSTOM_REQUIRE_UPPERCASE:
        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter.")
            
    if config.CUSTOM_SPECIAL_CHARS is not None:
        if not any(char in config.CUSTOM_SPECIAL_CHARS for char in password):
            errors.append(f"Password must contain at least one of the following characters: {config.CUSTOM_SPECIAL_CHARS}")

    if config.CUSTOM_USERNAME_NOT_DIFFERENT_FROM_MAIL:
        if valid_mail_address(username) and username.lower() != mail.lower():
            errors.append("Username cannot be an email address unless it matches your email address.")

    return errors if len(errors) > 0 else None
