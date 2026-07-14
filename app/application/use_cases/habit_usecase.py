from typing import Optional

from app.domain.entities.habit import Habit
from app.domain.repositories.habit_repository import HabitRepository


class HabitUseCase:
    def __init__(self, habit_repository: HabitRepository):
        self.habit_repository = habit_repository

    def create_habit(self, user_id: int, name: str, frequency: str) -> Habit:
        habit = Habit(id=None, user_id=user_id, name=name, frequency=frequency)
        habit.validate()
        return self.habit_repository.create(habit)

    def get_habit(self, habit_id: int) -> Optional[Habit]:
        return self.habit_repository.get_by_id(habit_id)

    def get_all_habits(self) -> list[Habit]:
        return self.habit_repository.get_all()

    def update_habit(self, habit: Habit) -> Habit:
        habit.validate()
        return self.habit_repository.update(habit)

    def complete_habit(self, habit_id: int) -> Habit:
        habit = self.habit_repository.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habit not found")
        habit.mark_completed()
        return self.habit_repository.update(habit)

    def reset_habit(self, habit_id: int) -> Habit:
        habit = self.habit_repository.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habit not found")
        habit.reset()
        return self.habit_repository.update(habit)

    def delete_habit(self, habit_id: int) -> bool:
        return self.habit_repository.delete(habit_id)
