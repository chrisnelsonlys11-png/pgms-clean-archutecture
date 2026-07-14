from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.goal import Goal
from app.domain.repositories.goal_repository import GoalRepository
from app.infrastructure.database.connection import GoalORM


class SqlAlchemyGoalRepository(GoalRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, goal: Goal) -> Goal:
        orm_goal = GoalORM(
            user_id=goal.user_id,
            title=goal.title,
            description=goal.description,
            start_date=goal.start_date,
            end_date=goal.end_date,
            status=goal.status,
        )
        self.db.add(orm_goal)
        self.db.commit()
        self.db.refresh(orm_goal)
        return self._to_entity(orm_goal)

    def get_by_id(self, goal_id: int) -> Optional[Goal]:
        orm_goal = self.db.query(GoalORM).filter(GoalORM.id == goal_id).first()
        return self._to_entity(orm_goal) if orm_goal else None

    def get_all(self) -> list[Goal]:
        return [self._to_entity(orm_goal) for orm_goal in self.db.query(GoalORM).all()]

    def update(self, goal: Goal) -> Goal:
        orm_goal = self.db.query(GoalORM).filter(GoalORM.id == goal.id).first()
        if orm_goal is None:
            raise ValueError("Goal not found")
        orm_goal.user_id = goal.user_id
        orm_goal.title = goal.title
        orm_goal.description = goal.description
        orm_goal.start_date = goal.start_date
        orm_goal.end_date = goal.end_date
        orm_goal.status = goal.status
        self.db.commit()
        self.db.refresh(orm_goal)
        return self._to_entity(orm_goal)

    def delete(self, goal_id: int) -> bool:
        orm_goal = self.db.query(GoalORM).filter(GoalORM.id == goal_id).first()
        if orm_goal is None:
            return False
        self.db.delete(orm_goal)
        self.db.commit()
        return True

    @staticmethod
    def _to_entity(orm_goal: Optional[GoalORM]) -> Optional[Goal]:
        if orm_goal is None:
            return None
        return Goal(
            id=orm_goal.id,
            user_id=orm_goal.user_id,
            title=orm_goal.title,
            description=orm_goal.description,
            start_date=orm_goal.start_date,
            end_date=orm_goal.end_date,
            status=orm_goal.status,
        )
