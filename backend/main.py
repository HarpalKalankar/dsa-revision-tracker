from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
app = FastAPI()
@app.get("/")
async def read_root():
    return {"Hello": "World"}


from database import get_db

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}