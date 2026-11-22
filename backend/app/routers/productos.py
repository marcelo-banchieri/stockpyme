from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria, Producto, Proveedor
from app.schemas import ProductoActualizar, ProductoCrear, ProductoLeer

router = APIRouter(prefix="/productos", tags=["Productos"])


def obtener_o_404(db: Session, producto_id: int) -> Producto:
    producto = db.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


def validar_relaciones(
    db: Session, categoria_id: int | None, proveedor_id: int | None
) -> None:
    if categoria_id is not None and db.get(Categoria, categoria_id) is None:
        raise HTTPException(status_code=400, detail="La categoría indicada no existe")
    if proveedor_id is not None and db.get(Proveedor, proveedor_id) is None:
        raise HTTPException(status_code=400, detail="El proveedor indicado no existe")


def guardar(db: Session, producto: Producto) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese SKU")
    db.refresh(producto)


@router.get("", response_model=list[ProductoLeer])
def listar_productos(
    buscar: str | None = None,
    categoria_id: int | None = None,
    solo_activos: bool = True,
    db: Session = Depends(get_db),
):
    consulta = select(Producto).order_by(Producto.nombre)
    if solo_activos:
        consulta = consulta.where(Producto.activo.is_(True))
    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)
    if buscar:
        patron = f"%{buscar}%"
        consulta = consulta.where(
            or_(Producto.nombre.ilike(patron), Producto.sku.ilike(patron))
        )
    return db.scalars(consulta).all()


@router.get("/stock-bajo", response_model=list[ProductoLeer])
def productos_stock_bajo(db: Session = Depends(get_db)):
    consulta = (
        select(Producto)
        .where(Producto.activo.is_(True))
        .where(Producto.stock_actual <= Producto.stock_minimo)
        .order_by(Producto.stock_actual)
    )
    return db.scalars(consulta).all()


@router.get("/{producto_id}", response_model=ProductoLeer)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, producto_id)


@router.post("", response_model=ProductoLeer, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCrear, db: Session = Depends(get_db)):
    validar_relaciones(db, datos.categoria_id, datos.proveedor_id)
    producto = Producto(**datos.model_dump())
    db.add(producto)
    guardar(db, producto)
    return producto


@router.patch("/{producto_id}", response_model=ProductoLeer)
def actualizar_producto(
    producto_id: int, datos: ProductoActualizar, db: Session = Depends(get_db)
):
    producto = obtener_o_404(db, producto_id)
    cambios = datos.model_dump(exclude_unset=True)
    validar_relaciones(db, cambios.get("categoria_id"), cambios.get("proveedor_id"))
    for campo, valor in cambios.items():
        setattr(producto, campo, valor)
    guardar(db, producto)
    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = obtener_o_404(db, producto_id)
    producto.activo = False
    db.commit()