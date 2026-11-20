import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

# Neon closes idle connections when the database sleeps. These settings stop
# the app from hanging on one of those dead connections.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=240,  # replace connections older than 4 minutes
    # give up after 10 s instead of hanging (Postgres only; tests use SQLite)
    connect_args={"connect_timeout": 10} if DATABASE_URL.startswith("postgresql") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()