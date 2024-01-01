from dependency_injector import containers, providers

from app.api.account.account_service import AccountService
from app.api.account.account_mock_service import AccountMockService

class Services(containers.DeclarativeContainer):
    """
    Container for services.
    """
    
    account_mock_service = providers.Factory(AccountMockService)
    account_service = providers.Factory(AccountService, account_service=account_mock_service)
    