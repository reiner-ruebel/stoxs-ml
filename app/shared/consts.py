class Consts:
    """ This class is used to store all constants of the application. """

    MAX_NAME_LENGTH = 32
    MAX_EMAIL_LENGTH = 64
    MIN_PASSWORD_LENGTH = 12
    MAX_PASSWORD_LENGTH = 32

    CONTROLLER_ROOT: str = "app/web/controllers"  # Root folder of all controllers.
    
    # The following constants are used for the database.
    DB_PRE_REGISTER = "pre_register"
    
    # Texts used in the application.
    ERROR = "error"
    CODE = "code"
    MESSAGE = "message"
    
    SWAGGER_MODEL = "SwaggerModel"
    RESPONSE_MODEL = "ResponseModel"
    
    # Extensions to avoid spelling errors.
    EXTENSION_SECURITY = "security"
    EXTENSION_SQLALCHEMY = "sqlalchemy"
    EXTENSION_MIGRATE = "migrate"
    EXTENSION_MARSHMALLOW = "marshmallow"
    EXTENSION_FLASK_ADMIN = "flask_admin"
    EXTENSION_MAIL = "mail"
    EXTENSION_JWT = "jwt"
