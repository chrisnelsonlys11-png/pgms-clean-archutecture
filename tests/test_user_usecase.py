from __future__ import annotations

from datetime import datetime

import pytest

from app.domain.entities.user import User
from app.application.use_cases.user_usecase import UserUseCase


class FakeUserRepository:
    def __init__(self, existing_user=None):
        self.existing_user = existing_user
        self.created_user = None
        self.updated_user = None
        self.deleted_user_id = None

    def create(self, user: User) -> User:
        user.id = 1
        self.created_user = user
        return user

    def get_by_id(self, user_id: int) -> User | None:
        if self.existing_user and self.existing_user.id == user_id:
            return self.existing_user
        return None

    def get_by_email(self, email: str) -> User | None:
        if self.existing_user and self.existing_user.email == email:
            return self.existing_user
        return None

    def get_all(self) -> list[User]:
        return [self.existing_user] if self.existing_user else []

    def update(self, user: User) -> User:
        self.updated_user = user
        return user

    def delete(self, user_id: int) -> bool:
        self.deleted_user_id = user_id
        return self.existing_user is not None and self.existing_user.id == user_id


def test_register_creates_new_user():
    repository = FakeUserRepository()
    usecase = UserUseCase(repository)

    user = usecase.register(
        full_name="Alice Dupont",
        email="alice@example.com",
        password="securepassword"
    )

    assert user.id == 1
    assert user.full_name == "Alice Dupont"
    assert user.email == "alice@example.com"
    assert repository.created_user is user


def test_register_duplicate_email_raises_value_error():
    existing = User(
        id=1,
        full_name="Bob Martin",
        email="bob@example.com",
        password="password123",
        created_at=datetime.now()
    )
    repository = FakeUserRepository(existing_user=existing)
    usecase = UserUseCase(repository)

    with pytest.raises(ValueError, match="Email already exists"):
        usecase.register(
            full_name="Robert Martin",
            email="bob@example.com",
            password="securepassword"
        )


def test_update_profile_raises_when_user_not_found():
    repository = FakeUserRepository()
    usecase = UserUseCase(repository)

    with pytest.raises(ValueError, match="User not found"):
        usecase.update_profile(user_id=99, full_name="Nouvel Nom")


def test_login_returns_user_by_email():
    existing = User(
        id=2,
        full_name="Claire Durand",
        email="claire@example.com",
        password="password123",
        created_at=datetime.now()
    )
    repository = FakeUserRepository(existing_user=existing)
    usecase = UserUseCase(repository)

    result = usecase.login(email="claire@example.com")

    assert result is existing


def test_delete_user_calls_repository():
    existing = User(
        id=3,
        full_name="Denis Petit",
        email="denis@example.com",
        password="password123",
        created_at=datetime.now()
    )
    repository = FakeUserRepository(existing_user=existing)
    usecase = UserUseCase(repository)

    deleted = usecase.delete_user(user_id=3)

    assert deleted is True
    assert repository.deleted_user_id == 3
