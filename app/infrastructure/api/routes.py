from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.use_cases.goal_usecase import GoalUseCase
from app.application.use_cases.habit_usecase import HabitUseCase
from app.application.use_cases.task_usecase import TaskUseCase
from app.application.use_cases.user_usecase import UserUseCase
from app.domain.entities.goal import Goal
from app.domain.entities.habit import Habit
from app.domain.entities.task import Task
from app.domain.entities.user import User
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.goal_repository import SqlAlchemyGoalRepository
from app.infrastructure.repositories.habit_repository import SqlAlchemyHabitRepository
from app.infrastructure.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

router = APIRouter()


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GoalCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None


class GoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    start_date: date
    end_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)


class HabitCreate(BaseModel):
    user_id: int
    name: str
    frequency: str


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None


class HabitResponse(BaseModel):
    id: int
    user_id: int
    name: str
    frequency: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    goal_id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskUpdate(BaseModel):
    goal_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    goal_id: int
    title: str
    description: Optional[str]
    completed: bool

    model_config = ConfigDict(from_attributes=True)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    use_case = UserUseCase(SqlAlchemyUserRepository(db))
    return use_case.register(user.full_name, user.email, user.password)


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    use_case = UserUseCase(SqlAlchemyUserRepository(db))
    return use_case.get_all_users()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    use_case = UserUseCase(SqlAlchemyUserRepository(db))
    user = use_case.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)) -> User:
    use_case = UserUseCase(SqlAlchemyUserRepository(db))
    return use_case.update_profile(user_id, user_data.full_name)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    use_case = UserUseCase(SqlAlchemyUserRepository(db))
    deleted = use_case.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)) -> Goal:
    use_case = GoalUseCase(SqlAlchemyGoalRepository(db))
    return use_case.create_goal(goal.user_id, goal.title, goal.description, goal.start_date, goal.end_date)


@router.get("/goals", response_model=list[GoalResponse])
def list_goals(db: Session = Depends(get_db)) -> list[Goal]:
    use_case = GoalUseCase(SqlAlchemyGoalRepository(db))
    return use_case.get_all_goals()


@router.put("/goals/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, goal_data: GoalUpdate, db: Session = Depends(get_db)) -> Goal:
    use_case = GoalUseCase(SqlAlchemyGoalRepository(db))
    return use_case.update_goal_details(
        goal_id,
        title=goal_data.title,
        description=goal_data.description,
        start_date=goal_data.start_date,
        end_date=goal_data.end_date,
        status=goal_data.status,
    )


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db)) -> None:
    use_case = GoalUseCase(SqlAlchemyGoalRepository(db))
    deleted = use_case.delete_goal(goal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Goal not found")


@router.post("/goals/{goal_id}/complete", response_model=GoalResponse)
def complete_goal(goal_id: int, db: Session = Depends(get_db)) -> Goal:
    use_case = GoalUseCase(SqlAlchemyGoalRepository(db))
    return use_case.complete_goal(goal_id)


@router.post("/goals/{goal_id}/reopen", response_model=GoalResponse)
def reopen_goal(goal_id: int, db: Session = Depends(get_db)) -> Goal:
    use_case = GoalUseCase(SqlAlchemyGoalRepository(db))
    return use_case.reopen_goal(goal_id)


@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)) -> Habit:
    use_case = HabitUseCase(SqlAlchemyHabitRepository(db))
    return use_case.create_habit(habit.user_id, habit.name, habit.frequency)


@router.get("/habits", response_model=list[HabitResponse])
def list_habits(db: Session = Depends(get_db)) -> list[Habit]:
    use_case = HabitUseCase(SqlAlchemyHabitRepository(db))
    return use_case.get_all_habits()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    use_case = TaskUseCase(SqlAlchemyTaskRepository(db))
    return use_case.create_task(Task(id=None, goal_id=task.goal_id, title=task.title, description=task.description, completed=task.completed))


@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)) -> list[Task]:
    use_case = TaskUseCase(SqlAlchemyTaskRepository(db))
    return use_case.get_all_tasks()


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    use_case = TaskUseCase(SqlAlchemyTaskRepository(db))
    return use_case.update_task_details(
        task_id,
        goal_id=task_data.goal_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
    )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    use_case = TaskUseCase(SqlAlchemyTaskRepository(db))
    deleted = use_case.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    use_case = TaskUseCase(SqlAlchemyTaskRepository(db))
    return use_case.complete_task(task_id)


@router.post("/tasks/{task_id}/reopen", response_model=TaskResponse)
def reopen_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    use_case = TaskUseCase(SqlAlchemyTaskRepository(db))
    return use_case.reopen_task(task_id)
