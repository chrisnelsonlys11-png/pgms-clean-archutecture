from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.database.connection import TaskORM


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        orm_task = TaskORM(
            goal_id=task.goal_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
        self.db.add(orm_task)
        self.db.commit()
        self.db.refresh(orm_task)
        return self._to_entity(orm_task)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        orm_task = self.db.query(TaskORM).filter(TaskORM.id == task_id).first()
        return self._to_entity(orm_task) if orm_task else None

    def get_all(self) -> list[Task]:
        return [self._to_entity(orm_task) for orm_task in self.db.query(TaskORM).all()]

    def update(self, task: Task) -> Task:
        orm_task = self.db.query(TaskORM).filter(TaskORM.id == task.id).first()
        if orm_task is None:
            raise ValueError("Task not found")
        orm_task.goal_id = task.goal_id
        orm_task.title = task.title
        orm_task.description = task.description
        orm_task.completed = task.completed
        self.db.commit()
        self.db.refresh(orm_task)
        return self._to_entity(orm_task)

    def delete(self, task_id: int) -> bool:
        orm_task = self.db.query(TaskORM).filter(TaskORM.id == task_id).first()
        if orm_task is None:
            return False
        self.db.delete(orm_task)
        self.db.commit()
        return True

    @staticmethod
    def _to_entity(orm_task: Optional[TaskORM]) -> Optional[Task]:
        if orm_task is None:
            return None
        return Task(
            id=orm_task.id,
            goal_id=orm_task.goal_id,
            title=orm_task.title,
            description=orm_task.description,
            completed=orm_task.completed,
        )
