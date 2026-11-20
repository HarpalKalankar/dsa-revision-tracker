from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models import Problem, Revision, User
from security import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])


class TopicStat(BaseModel):
    topic: str
    solved: int
    hard_revisions: int


@router.get("/topics", response_model=list[TopicStat])
def topic_stats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hard = func.count(Revision.id).filter(Revision.result == "hard")
    query = (
        select(
            Problem.topic,
            func.count(func.distinct(Problem.id)),
            hard,
        )
        .outerjoin(Revision, Revision.problem_id == Problem.id)
        .where(Problem.user_id == user.id)
        .group_by(Problem.topic)
        .order_by(hard.desc(), Problem.topic)  # weakest topics first
    )
    return [
        TopicStat(topic=topic, solved=solved, hard_revisions=hard_count)
        for topic, solved, hard_count in db.execute(query)
    ]