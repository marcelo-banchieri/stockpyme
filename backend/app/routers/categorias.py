from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria
from app.schemas import CategoriaCrear, CategoriaLeer

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("", response_model=list[CategoriaLeer])
def listar_categorias(db: Session = Depends(get_db)):
    return db.scalars(select(Categoria).order_by(Categoria.nombre)).all()


@router.get("/{categoria_id}", response_model=CategoriaLeer)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post("", response_model=CategoriaLeer, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CategoriaCrear, db: Session = Depends(get_db)):
    categoria = Categoria(nombre=datos.nombre)
    db.add(categoria)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Ya existe una categoría con ese nombre"
        )
    db.refresh(categoria)
    return categoria


@router.patch("/{categoria_id}", response_model=CategoriaLeer)
def actualizar_categoria(
    categoria_id: int, datos: CategoriaCrear, db: Session = Depends(get_db)
):
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.nombre = datos.nombre
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Ya existe una categoría con ese nombre"
        )
    db.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoria.productos:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: la categoría tiene productos asociados",
        )
    db.delete(categoria)
    db.commit()