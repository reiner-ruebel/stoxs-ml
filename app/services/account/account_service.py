from .iaccount_service import IAccountService
from app.services.account.register_payload import RegisterPayload
from .register_result import RegisterResult


class AccountService(IAccountService):
    def __init__(self, account_service: IAccountService) -> None:
        self._account_service = account_service
        
    def register(self, payload: RegisterPayload) -> RegisterResult:
        return self._account_service.register(payload)
