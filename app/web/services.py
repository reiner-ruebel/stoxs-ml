from dependency_injector import containers, providers

from app.services import IAccountService
from app.services import AccountMockService

class Services(containers.DeclarativeContainer):
    """
    Container for services.
    """
    
    account_mock_service = providers.Factory(AccountMockService)
    account_service = providers.Factory(IAccountService, account_service=account_mock_service)
    