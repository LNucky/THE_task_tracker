from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        return await self.repo.save(task)

    async def get_tasks(self) -> list[Task]:
        return await self.repo.get_all()

    async def get_task(self, task_id: int) -> Task:
        task = await self.repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Задача {task_id} не найдена")
        return task

    async def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        task = await self.get_task(task_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            if value is None:
                raise ValueError(f"Поле {field} не может быть null")
            setattr(task, field, value)
        return await self.repo.save(task)

    async def delete_task(self, task_id: int) -> None:
        task = await self.get_task(task_id)
        await self.repo.delete(task)
