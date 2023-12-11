class Consts:
    """ This class is used to store all constants of the application. """

    MAX_NAME_LENGTH: int = 32
    MAX_EMAIL_LENGTH: int = 64
    MIN_PASSWORD_LENGTH: int = 12
    MAX_PASSWORD_LENGTH: int = 32

    BP_ROOT: str = "app/api" # Root folder of all blueprints.
    ENDPOINTS: str = "endpoints" # The folder name where all endpoints are located inside a container (blueprint)
    MIDDLEWARE: str = "app/core/middlewares" # The name of the middleware module in a middleware directory.
    
    # The following constants are used for the database.
    DB_PRE_REGISTER: str = "pre_register"
