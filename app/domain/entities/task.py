from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: Optional[int]
    goal_id: int
    title: str
    description: Optional[str]
    completed: bool = False

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Task title cannot be empty.")

    def complete(self) -> None:
        self.completed = True

    def reopen(self) -> None:
        self.completed = False
