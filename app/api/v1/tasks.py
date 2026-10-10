from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_task_service
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create_task(data)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        return await service.get_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, data: TaskUpdate, service: TaskService = Depends(get_task_service)):
    try:
        return await service.update_task(task_id, data)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        await service.delete_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
