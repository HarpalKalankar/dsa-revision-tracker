from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Problem, Revision, User
from revision_logic import first_due
from schemas import ProblemCreate, ProblemOut, ProblemUpdate
from security import get_current_user

router = APIRouter(prefix="/problems", tags=["problems"])


def get_own_problem(problem_id: int, user: User, db: Session) -> Problem:
    problem = db.get(Problem, problem_id)
    # Same 404 for "doesn't exist" and "belongs to someone else",
    # so users can't discover other people's problem ids
    if problem is None or problem.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Problem not found")
    return problem


@router.post("", response_model=ProblemOut, status_code=status.HTTP_201_CREATED)
def create_problem(
    data: ProblemCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = Problem(
        user_id=user.id,
        title=data.title,
        url=str(data.url),
        topic=data.topic,
        difficulty=data.difficulty,
        notes=data.notes,
        solved_on=data.solved_on,
    )
    # Every new problem gets its first revision, due the next day
    problem.revisions.append(Revision(stage=1, due_on=first_due(data.solved_on)))
    db.add(problem)
    try:
        db.commit()
    except IntegrityError:  # the (user_id, url) unique constraint
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "You already logged this problem")
    db.refresh(problem)
    return problem


@router.get("", response_model=list[ProblemOut])
def list_problems(
    topic: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        select(Problem)
        .where(Problem.user_id == user.id)
        .order_by(Problem.solved_on.desc(), Problem.id.desc())
    )
    if topic:
        query = query.where(Problem.topic == topic)
    return db.scalars(query).all()


@router.get("/{problem_id}", response_model=ProblemOut)
def get_problem(
    problem_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_own_problem(problem_id, user, db)


@router.patch("/{problem_id}", response_model=ProblemOut)
def update_problem(
    problem_id: int,
    data: ProblemUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = get_own_problem(problem_id, user, db)
    # Only change the fields the request actually sent
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(problem, field, value)
    db.commit()
    db.refresh(problem)
    return problem


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(
    problem_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = get_own_problem(problem_id, user, db)
    db.delete(problem)  # its revisions go too (cascade)
    db.commit()