from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.connection import UserORM


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        orm_user = UserORM(
            full_name=user.full_name,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
        )
        self.db.add(orm_user)
        self.db.commit()
        self.db.refresh(orm_user)
        return self._to_entity(orm_user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        orm_user = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        return self._to_entity(orm_user) if orm_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        orm_user = self.db.query(UserORM).filter(UserORM.email == email).first()
        return self._to_entity(orm_user) if orm_user else None

    def get_all(self) -> list[User]:
        return [self._to_entity(orm_user) for orm_user in self.db.query(UserORM).all()]

    def update(self, user: User) -> User:
        orm_user = self.db.query(UserORM).filter(UserORM.id == user.id).first()
        if orm_user is None:
            raise ValueError("User not found")
        orm_user.full_name = user.full_name
        orm_user.email = user.email
        orm_user.password = user.password
        orm_user.created_at = user.created_at
        self.db.commit()
        self.db.refresh(orm_user)
        return self._to_entity(orm_user)

    def delete(self, user_id: int) -> bool:
        orm_user = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if orm_user is None:
            return False
        self.db.delete(orm_user)
        self.db.commit()
        return True

    @staticmethod
    def _to_entity(orm_user: Optional[UserORM]) -> Optional[User]:
        if orm_user is None:
            return None
        return User(
            id=orm_user.id,
            full_name=orm_user.full_name,
            email=orm_user.email,
            password=orm_user.password,
            created_at=orm_user.created_at,
        )
