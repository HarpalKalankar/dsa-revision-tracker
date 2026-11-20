from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, contains_eager

from database import get_db
from models import Problem, Revision, User
from revision_logic import next_revision, today_ist
from schemas import RevisionDone, RevisionOut, RevisionResult
from security import get_current_user

router = APIRouter(prefix="/revisions", tags=["revisions"])


@router.get("/today", response_model=list[RevisionOut])
def today_queue(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = (
        select(Revision)
        .join(Revision.problem)
        .where(
            Problem.user_id == user.id,
            Revision.due_on <= today_ist(),
            Revision.completed_at.is_(None),
        )
        # Load each revision's problem in the same query (avoids N+1)
        .options(contains_eager(Revision.problem))
        .order_by(Revision.due_on, Revision.id)
    )
    return db.scalars(query).all()


@router.post("/{revision_id}/complete", response_model=RevisionDone)
def complete_revision(
    revision_id: int,
    data: RevisionResult,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    revision = db.get(Revision, revision_id)
    if revision is None or revision.problem.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Revision not found")
    if revision.completed_at is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Revision already completed")

    revision.completed_at = func.now()
    revision.result = data.result

    upcoming = next_revision(revision.stage, data.result, today_ist())
    if upcoming:
        stage, due_on = upcoming
        db.add(Revision(problem_id=revision.problem_id, stage=stage, due_on=due_on))
    # Marking this one done and adding the next happen in one transaction
    db.commit()

    if upcoming:
        return RevisionDone(next_stage=upcoming[0], next_due_on=upcoming[1])
    return RevisionDone(next_stage=None, next_due_on=None)