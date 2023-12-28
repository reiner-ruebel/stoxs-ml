from typing import Optional

from flask_security import password_complexity_validator

from app.core.application.app_components import AppComponents as C
from app.core.security.user import User
from app.core.mail.mail import AppMail


class SecurityService:
    """Service for security related tasks."""

    #
    # data retrieval
    #

    @staticmethod
    def user_exist(username: str, email: str) -> bool:
        """ Checks if a user with the given username exists. """

        return User.query.filter((User.username == username) | (User.email == email)).count() > 0


    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """ Returns the user with the given username. """

        return User.query.filter(User.username == username).first()


    #
    # custom policies
    #

    @staticmethod
    def user_policy_checker(password: str, mail: str, username: Optional[str]) -> Optional[list[str]]:
        """Checks if user credentials meet custom requirements."""

        config = C.config_object
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

        if username and config.CUSTOM_USERNAME_NOT_DIFFERENT_FROM_MAIL:
            if AppMail.valid_email_address(username) and username.lower() != mail.lower():
                errors.append("Username cannot be an email address unless it matches your email address.")

        validation_msgs = password_complexity_validator(password, is_register = True)
        if validation_msgs:
            errors.extend(validation_msgs)

        return errors if len(errors) > 0 else None
