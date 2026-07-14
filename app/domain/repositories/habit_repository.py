from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.habit import Habit


class HabitRepository(ABC):
    @abstractmethod
    def create(self, habit: Habit) -> Habit:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, habit_id: int) -> Optional[Habit]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Habit]:
        raise NotImplementedError

    @abstractmethod
    def update(self, habit: Habit) -> Habit:
        raise NotImplementedError

    @abstractmethod
    def delete(self, habit_id: int) -> bool:
        raise NotImplementedError
