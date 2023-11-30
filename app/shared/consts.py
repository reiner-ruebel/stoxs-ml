class Consts:
    """ This class is used to store all constants of the application. """

    MAX_NAME_LENGTH: int = 32
    MAX_EMAIL_LENGTH: int = 64
    MIN_PASSWORD_LENGTH: int = 12
    MAX_PASSWORD_LENGTH: int = 32

    BP_ROOT: str = "app/api" # Root folder of all blueprints.
    ENDPOINTS: str = "endpoints" # The folder name where all endpoints are located inside a container (blueprint)
