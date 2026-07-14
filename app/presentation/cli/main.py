from __future__ import annotations

from datetime import date

from app.application.use_cases.goal_usecase import GoalUseCase
from app.application.use_cases.task_usecase import TaskUseCase
from app.application.use_cases.user_usecase import UserUseCase
from app.domain.entities.task import Task
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.repositories.goal_repository import SqlAlchemyGoalRepository
from app.infrastructure.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.repositories.user_repository import SqlAlchemyUserRepository


def _ensure_default_user(db):
    user_use_case = UserUseCase(SqlAlchemyUserRepository(db))
    user = user_use_case.login("pgms@example.com")
    if user is None:
        return user_use_case.register("PGMS User", "pgms@example.com", "pgms1234")
    return user


def _prompt_text(prompt: str) -> str:
    return input(prompt).strip()


def _prompt_date(prompt: str) -> date:
    value = _prompt_text(prompt)
    return date.fromisoformat(value)


def main() -> None:
    print("PGMS CLI")
    print("Welcome to your personal goal manager")

    db = SessionLocal()
    try:
        user = _ensure_default_user(db)

        while True:
            print("\n1. Create goal")
            print("2. List goals")
            print("3. Create task")
            print("4. List tasks")
            print("5. Complete goal")
            print("6. Complete task")
            print("0. Exit")

            choice = _prompt_text("Choose an option: ")
            if choice in {"0", "q", "quit"}:
                print("Goodbye")
                break

            if choice == "1":
                title = _prompt_text("Goal title: ")
                description = _prompt_text("Description (optional): ")
                start_date = _prompt_date("Start date (YYYY-MM-DD): ")
                end_date = _prompt_date("End date (YYYY-MM-DD): ")
                goal = GoalUseCase(SqlAlchemyGoalRepository(db)).create_goal(
                    user.id,
                    title,
                    description or None,
                    start_date,
                    end_date,
                )
                print(f"Goal created: {goal.title} ({goal.status})")
            elif choice == "2":
                goals = GoalUseCase(SqlAlchemyGoalRepository(db)).get_all_goals()
                if not goals:
                    print("No goals yet.")
                else:
                    for goal in goals:
                        print(f"- {goal.id}: {goal.title} [{goal.status}]")
            elif choice == "3":
                goal_id = int(_prompt_text("Goal ID: "))
                title = _prompt_text("Task title: ")
                description = _prompt_text("Description (optional): ")
                task = TaskUseCase(SqlAlchemyTaskRepository(db)).create_task(
                    Task(
                        id=None,
                        goal_id=goal_id,
                        title=title,
                        description=description or None,
                        completed=False,
                    )
                )
                print(f"Task created: {task.title}")
            elif choice == "4":
                tasks = TaskUseCase(SqlAlchemyTaskRepository(db)).get_all_tasks()
                if not tasks:
                    print("No tasks yet.")
                else:
                    for task in tasks:
                        print(f"- {task.id}: {task.title} [{'done' if task.completed else 'pending'}]")
            elif choice == "5":
                goal_id = int(_prompt_text("Goal ID: "))
                GoalUseCase(SqlAlchemyGoalRepository(db)).complete_goal(goal_id)
                print("Goal marked as completed")
            elif choice == "6":
                task_id = int(_prompt_text("Task ID: "))
                TaskUseCase(SqlAlchemyTaskRepository(db)).complete_task(task_id)
                print("Task marked as completed")
            else:
                print("Invalid choice")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye")
    finally:
        db.close()


if __name__ == "__main__":
    main()
