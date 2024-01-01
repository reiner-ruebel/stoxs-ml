from .iaccount_service import IAccountService
from .register_payload import RegisterPayload
from .register_result import RegisterResult

class AccountMockService(IAccountService):
    def register(self, payload: RegisterPayload) -> RegisterResult:
        if payload.firstname != "Hugo":
            result = RegisterResult(True, "User registered successfully")
        else:
            result = RegisterResult(False, "User already exists")

        return result
