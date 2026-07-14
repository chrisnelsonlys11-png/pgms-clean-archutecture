from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Goal:
    id: Optional[int]
    user_id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date
    status: str = "Pending"

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Goal title cannot be empty.")
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than the start date.")

    def complete(self) -> None:
        self.status = "Completed"

    def reopen(self) -> None:
        self.status = "Pending"
