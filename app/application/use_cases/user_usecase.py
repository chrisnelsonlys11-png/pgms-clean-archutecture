from datetime import datetime
from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, full_name: str, email: str, password: str) -> User:
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already exists")

        user = User(
            id=None,
            full_name=full_name,
            email=email,
            password=password,
            created_at=datetime.now(),
        )
        user.change_password(password)
        return self.user_repository.create(user)

    def login(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all()

    def update_profile(self, user_id: int, full_name: str) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        user.update_name(full_name)
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)
