from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    full_name: str
    email: str
    password: str
    created_at: datetime

    def update_name(self, full_name: str) -> None:
        if not full_name.strip():
            raise ValueError("Full name cannot be empty.")
        self.full_name = full_name

    def change_password(self, new_password: str) -> None:
        if len(new_password) < 8:
            raise ValueError("Password must contain at least 8 characters.")
        self.password = new_password
