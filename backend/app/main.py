from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import categorias, productos, proveedores

app = FastAPI(title="StockPyme")

app.include_router(categorias.router)
app.include_router(proveedores.router)
app.include_router(productos.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.get("/salud-db")
def salud_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"base_de_datos": "ok"}