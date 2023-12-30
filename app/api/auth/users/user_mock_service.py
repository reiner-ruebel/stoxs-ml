from .iuser_service import IUserService

from .models.user import User

class UserMockService(IUserService):
    def __init__(self) -> None:
        pass

    def get_all(self):
        return []

    def get_by_id(self, user_id: int) -> User:
        return User()

    def get_by_email(self, email):
        return User()

    def create(self, user):
        return User()

    def update(self, user_id, user):
        return User()

    def delete(self, user_id):
        return User()
