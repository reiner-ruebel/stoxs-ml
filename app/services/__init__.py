from dependency_injector import containers, providers

from .account.iaccount_service import IAccountService
from .account.account_service import AccountService
from .account.account_mock_service import AccountMockService
from .account.register_payload import RegisterPayload
from .account.register_result import RegisterResult


class Services(containers.DeclarativeContainer):
    """
    Container for services.
    """
    # for later
    #   a) create all services, if they exist (or better: create a service factory)
    #   b) get the effective service from the config
    
    account_mock_service = providers.Factory(AccountMockService)
    account_service = providers.Factory(AccountService, account_service=account_mock_service)

__all__ = ['IAccountService', 'RegisterPayload', 'Services', 'RegisterResult']
