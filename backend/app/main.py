from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

app = FastAPI(title="StockPyme")


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.get("/salud-db")
def salud_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"base_de_datos": "ok"}