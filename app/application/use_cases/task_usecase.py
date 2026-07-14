from typing import Optional

from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository


class TaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task: Task) -> Task:
        task.validate()
        return self.task_repository.create(task)

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.task_repository.get_all()

    def update_task(self, task_id: int, updated_task: Task) -> Optional[Task]:
        existing_task = self.task_repository.get_by_id(task_id)
        if existing_task is None:
            return None
        updated_task.id = task_id
        updated_task.validate()
        return self.task_repository.update(updated_task)

    def update_task_details(
        self,
        task_id: int,
        goal_id: Optional[int] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")

        if goal_id is not None:
            task.goal_id = goal_id
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        task.validate()
        return self.task_repository.update(task)

    def complete_task(self, task_id: int) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        task.complete()
        return self.task_repository.update(task)

    def reopen_task(self, task_id: int) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        task.reopen()
        return self.task_repository.update(task)

    def delete_task(self, task_id: int) -> bool:
        existing_task = self.task_repository.get_by_id(task_id)
        if existing_task is None:
            return False
        return self.task_repository.delete(task_id)
