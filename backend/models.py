from datetime import date, datetime

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    problems: Mapped[list["Problem"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Problem(Base):
    __tablename__ = "problems"
    __table_args__ = (UniqueConstraint("user_id", "url"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(500))
    topic: Mapped[str] = mapped_column(String(50))       # e.g. "Arrays", "Graphs"
    difficulty: Mapped[str] = mapped_column(String(10))  # "Easy", "Medium", "Hard"
    notes: Mapped[str | None] = mapped_column(Text)
    solved_on: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="problems")
    revisions: Mapped[list["Revision"]] = relationship(
        back_populates="problem", cascade="all, delete-orphan"
    )


class Revision(Base):
    __tablename__ = "revisions"
    __table_args__ = (Index("ix_revisions_due", "due_on", "completed_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problems.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[int]                     # 1, 2, 3, 4 = day 1, 3, 7, 21
    due_on: Mapped[date]
    completed_at: Mapped[datetime | None]  # empty until revised
    result: Mapped[str | None] = mapped_column(String(10))  # "easy" or "hard"

    problem: Mapped["Problem"] = relationship(back_populates="revisions")
    