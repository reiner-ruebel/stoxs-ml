from .models.user import User
from .iuser_service import IUserService


class UserService:
    _user_service: IUserService

    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service


    def get_all(self):
        return self._user_service.get_all()

    def get_by_id(self, user_id: int) -> User:
        return self._user_service.get_by_id(user_id)

    def get_by_email(self, email):
        return self._user_service.get_by_email(email)

    def create(self, user):
        return self._user_service.create(user)

    def update(self, user_id, user):
        return self._user_service.update(user_id, user)

    def delete(self, user_id):
        return self._user_service.delete(user_id)
    
