from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    id: Optional[int]
    user_id: int
    name: str
    frequency: str
    completed: bool = False

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Habit name cannot be empty.")
        if self.frequency not in {"Daily", "Weekly", "Monthly"}:
            raise ValueError("Frequency must be Daily, Weekly or Monthly.")

    def mark_completed(self) -> None:
        self.completed = True

    def reset(self) -> None:
        self.completed = False
