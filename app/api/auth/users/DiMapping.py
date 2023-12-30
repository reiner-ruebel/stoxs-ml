from dependency_injector import containers, providers

from .user_mock_service import UserMockService
from .user_service import UserService

class DiMapping(containers.DeclarativeContainer):
    user_mock_service = providers.Factory(UserMockService)
    user_service = providers.Factory(UserService, user_service = user_mock_service)
    