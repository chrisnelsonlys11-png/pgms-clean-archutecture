from datetime import date
from typing import Optional

from app.domain.entities.goal import Goal
from app.domain.repositories.goal_repository import GoalRepository


class GoalUseCase:
    def __init__(self, goal_repository: GoalRepository):
        self.goal_repository = goal_repository

    def create_goal(self, user_id: int, title: str, description: Optional[str], start_date: date, end_date: date) -> Goal:
        goal = Goal(
            id=None,
            user_id=user_id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        goal.validate()
        return self.goal_repository.create(goal)

    def get_goal(self, goal_id: int) -> Optional[Goal]:
        return self.goal_repository.get_by_id(goal_id)

    def get_all_goals(self) -> list[Goal]:
        return self.goal_repository.get_all()

    def update_goal(self, goal: Goal) -> Goal:
        goal.validate()
        return self.goal_repository.update(goal)

    def update_goal_details(
        self,
        goal_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: Optional[str] = None,
    ) -> Goal:
        goal = self.goal_repository.get_by_id(goal_id)
        if goal is None:
            raise ValueError("Goal not found")

        if title is not None:
            goal.title = title
        if description is not None:
            goal.description = description
        if start_date is not None:
            goal.start_date = start_date
        if end_date is not None:
            goal.end_date = end_date
        if status is not None:
            goal.status = status

        goal.validate()
        return self.goal_repository.update(goal)

    def complete_goal(self, goal_id: int) -> Goal:
        goal = self.goal_repository.get_by_id(goal_id)
        if goal is None:
            raise ValueError("Goal not found")
        goal.complete()
        return self.goal_repository.update(goal)

    def reopen_goal(self, goal_id: int) -> Goal:
        goal = self.goal_repository.get_by_id(goal_id)
        if goal is None:
            raise ValueError("Goal not found")
        goal.reopen()
        return self.goal_repository.update(goal)

    def delete_goal(self, goal_id: int) -> bool:
        return self.goal_repository.delete(goal_id)
