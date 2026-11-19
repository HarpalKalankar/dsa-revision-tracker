from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

Topic = Literal[
    "Arrays", "Strings", "Hashing", "Two Pointers", "Sliding Window",
    "Linked List", "Stack", "Queue", "Binary Search", "Recursion",
    "Trees", "Heaps", "Graphs", "Backtracking", "Dynamic Programming",
    "Greedy", "Other",
]
Difficulty = Literal["Easy", "Medium", "Hard"]


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=72)  # bcrypt's limit is 72 bytes


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProblemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    url: HttpUrl
    topic: Topic
    difficulty: Difficulty
    notes: str | None = None
    solved_on: date


class ProblemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    topic: Topic | None = None
    difficulty: Difficulty | None = None
    notes: str | None = None


class ProblemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    topic: str
    difficulty: str
    notes: str | None
    solved_on: date


class RevisionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stage: int
    due_on: date
    problem: ProblemOut


class RevisionResult(BaseModel):
    result: Literal["easy", "hard"]


class RevisionDone(BaseModel):
    next_stage: int | None
    next_due_on: date | None