from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from routers import auth, problems

app = FastAPI(title="DSA Revision Tracker")


app.include_router(auth.router)
app.include_router(problems.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}