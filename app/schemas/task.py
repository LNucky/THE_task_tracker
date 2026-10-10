from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Priority = Annotated[int, Field(ge=1, le=5)]


class TaskCreate(BaseModel):
    title: Title
    priority: Priority = 1
    done: bool = False


class TaskUpdate(BaseModel):
    title: Title | None = None
    priority: Priority | None = None
    done: bool | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    priority: int
    done: bool
