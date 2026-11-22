import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)

    productos: Mapped[list["Producto"]] = relationship(back_populates="categoria")


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    telefono: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(150))
    activo: Mapped[bool] = mapped_column(default=True)

    productos: Mapped[list["Producto"]] = relationship(back_populates="proveedor")


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    nombre: Mapped[str] = mapped_column(String(150))
    descripcion: Mapped[str | None] = mapped_column(String(500))
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedores.id"))
    precio_costo: Mapped[int]
    precio_venta: Mapped[int]
    stock_actual: Mapped[int] = mapped_column(default=0)
    stock_minimo: Mapped[int] = mapped_column(default=0)
    activo: Mapped[bool] = mapped_column(default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    categoria: Mapped["Categoria"] = relationship(back_populates="productos")
    proveedor: Mapped["Proveedor | None"] = relationship(back_populates="productos")

class RolUsuario(str, enum.Enum):
    admin = "admin"
    vendedor = "vendedor"


class TipoMovimiento(str, enum.Enum):
    entrada = "entrada"
    salida = "salida"
    ajuste = "ajuste"
    venta = "venta"
    anulacion = "anulacion"


class MetodoPago(str, enum.Enum):
    efectivo = "efectivo"
    debito = "debito"
    credito = "credito"
    transferencia = "transferencia"


class EstadoVenta(str, enum.Enum):
    completada = "completada"
    anulada = "anulada"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario), default=RolUsuario.vendedor)
    activo: Mapped[bool] = mapped_column(default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    fecha: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    total: Mapped[int] = mapped_column(default=0)
    metodo_pago: Mapped[MetodoPago] = mapped_column(Enum(MetodoPago))
    estado: Mapped[EstadoVenta] = mapped_column(
        Enum(EstadoVenta), default=EstadoVenta.completada
    )

    usuario: Mapped["Usuario"] = relationship()
    detalles: Mapped[list["DetalleVenta"]] = relationship(back_populates="venta")


class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    cantidad: Mapped[int]
    precio_unitario: Mapped[int]
    subtotal: Mapped[int]

    venta: Mapped["Venta"] = relationship(back_populates="detalles")
    producto: Mapped["Producto"] = relationship()


class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    tipo: Mapped[TipoMovimiento] = mapped_column(Enum(TipoMovimiento))
    cantidad: Mapped[int]
    motivo: Mapped[str | None] = mapped_column(String(255))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    venta_id: Mapped[int | None] = mapped_column(ForeignKey("ventas.id"))
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    producto: Mapped["Producto"] = relationship()
    usuario: Mapped["Usuario"] = relationship()
    venta: Mapped["Venta | None"] = relationship()