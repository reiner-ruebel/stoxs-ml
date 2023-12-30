from abc import ABC, abstractmethod

from .models.user import User


class IUserService(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def create(self, user):
        pass

    @abstractmethod
    def update(self, user_id, user):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
