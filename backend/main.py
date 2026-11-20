import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from routers import auth, problems, revisions, stats

app = FastAPI(title="DSA Revision Tracker")

# Which websites may call this API from a browser.
# Locally that's Vite's dev server. On Render, set FRONTEND_ORIGINS.
origins = os.environ.get("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(problems.router)
app.include_router(revisions.router)
app.include_router(stats.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}