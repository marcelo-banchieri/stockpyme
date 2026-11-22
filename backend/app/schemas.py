from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CategoriaCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)


class CategoriaLeer(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)

class ProveedorCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    telefono: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=150)


class ProveedorActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    telefono: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=150)
    activo: bool | None = None


class ProveedorLeer(BaseModel):
    id: int
    nombre: str
    telefono: str | None
    email: str | None
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class ProductoCrear(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=500)
    categoria_id: int
    proveedor_id: int | None = None
    precio_costo: int = Field(ge=0)
    precio_venta: int = Field(ge=0)
    stock_minimo: int = Field(default=0, ge=0)


class ProductoActualizar(BaseModel):
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=500)
    categoria_id: int | None = None
    proveedor_id: int | None = None
    precio_costo: int | None = Field(default=None, ge=0)
    precio_venta: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    activo: bool | None = None


class ProductoLeer(BaseModel):
    id: int
    sku: str
    nombre: str
    descripcion: str | None
    precio_costo: int
    precio_venta: int
    stock_actual: int
    stock_minimo: int
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
    categoria: CategoriaLeer
    proveedor: ProveedorLeer | None

    model_config = ConfigDict(from_attributes=True)