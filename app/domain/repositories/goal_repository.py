from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.goal import Goal


class GoalRepository(ABC):
    @abstractmethod
    def create(self, goal: Goal) -> Goal:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, goal_id: int) -> Optional[Goal]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Goal]:
        raise NotImplementedError

    @abstractmethod
    def update(self, goal: Goal) -> Goal:
        raise NotImplementedError

    @abstractmethod
    def delete(self, goal_id: int) -> bool:
        raise NotImplementedError
