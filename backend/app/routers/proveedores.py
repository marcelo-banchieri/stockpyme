from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Proveedor
from app.schemas import ProveedorActualizar, ProveedorCrear, ProveedorLeer

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


def obtener_o_404(db: Session, proveedor_id: int) -> Proveedor:
    proveedor = db.get(Proveedor, proveedor_id)
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.get("", response_model=list[ProveedorLeer])
def listar_proveedores(solo_activos: bool = True, db: Session = Depends(get_db)):
    consulta = select(Proveedor).order_by(Proveedor.nombre)
    if solo_activos:
        consulta = consulta.where(Proveedor.activo.is_(True))
    return db.scalars(consulta).all()


@router.get("/{proveedor_id}", response_model=ProveedorLeer)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, proveedor_id)


@router.post("", response_model=ProveedorLeer, status_code=status.HTTP_201_CREATED)
def crear_proveedor(datos: ProveedorCrear, db: Session = Depends(get_db)):
    proveedor = Proveedor(**datos.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


@router.patch("/{proveedor_id}", response_model=ProveedorLeer)
def actualizar_proveedor(
    proveedor_id: int, datos: ProveedorActualizar, db: Session = Depends(get_db)
):
    proveedor = obtener_o_404(db, proveedor_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(proveedor, campo, valor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


@router.delete("/{proveedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = obtener_o_404(db, proveedor_id)
    proveedor.activo = False
    db.commit()