from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


async def get_db() -> AsyncIterator[AsyncSession]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


def get_task_repository(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repo)
