from sqlalchemy import Boolean, Integer, String, false, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
