from typing import List

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        existing_user = self.user_repository.get_user_by_email(user.email)
        if existing_user:
            raise Exception("User with that email already exists")
        return self.user_repository.create_user(user)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_users(self) -> List[User]:
        return self.user_repository.get_users()

    def update_user(self, user_id: int, user: User) -> User:
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise Exception("User not found")
        user.id = user_id
        return self.user_repository.update_user(user)

    def delete_user(self, user_id: int) -> bool:
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise Exception("User not found")
        return self.user_repository.delete_user(user_id)
