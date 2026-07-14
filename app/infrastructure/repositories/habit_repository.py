from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.habit import Habit
from app.domain.repositories.habit_repository import HabitRepository
from app.infrastructure.database.connection import HabitORM


class SqlAlchemyHabitRepository(HabitRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, habit: Habit) -> Habit:
        orm_habit = HabitORM(
            user_id=habit.user_id,
            name=habit.name,
            frequency=habit.frequency,
            completed=habit.completed,
        )
        self.db.add(orm_habit)
        self.db.commit()
        self.db.refresh(orm_habit)
        return self._to_entity(orm_habit)

    def get_by_id(self, habit_id: int) -> Optional[Habit]:
        orm_habit = self.db.query(HabitORM).filter(HabitORM.id == habit_id).first()
        return self._to_entity(orm_habit) if orm_habit else None

    def get_all(self) -> list[Habit]:
        return [self._to_entity(orm_habit) for orm_habit in self.db.query(HabitORM).all()]

    def update(self, habit: Habit) -> Habit:
        orm_habit = self.db.query(HabitORM).filter(HabitORM.id == habit.id).first()
        if orm_habit is None:
            raise ValueError("Habit not found")
        orm_habit.user_id = habit.user_id
        orm_habit.name = habit.name
        orm_habit.frequency = habit.frequency
        orm_habit.completed = habit.completed
        self.db.commit()
        self.db.refresh(orm_habit)
        return self._to_entity(orm_habit)

    def delete(self, habit_id: int) -> bool:
        orm_habit = self.db.query(HabitORM).filter(HabitORM.id == habit_id).first()
        if orm_habit is None:
            return False
        self.db.delete(orm_habit)
        self.db.commit()
        return True

    @staticmethod
    def _to_entity(orm_habit: Optional[HabitORM]) -> Optional[Habit]:
        if orm_habit is None:
            return None
        return Habit(
            id=orm_habit.id,
            user_id=orm_habit.user_id,
            name=orm_habit.name,
            frequency=orm_habit.frequency,
            completed=orm_habit.completed,
        )
