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