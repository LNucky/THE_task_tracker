from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Task]:
        result = await self.db.scalars(select(Task).order_by(Task.id))
        return list(result)

    async def get_by_id(self, task_id: int) -> Task | None:
        return await self.db.get(Task, task_id)

    async def save(self, task: Task) -> Task:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()
