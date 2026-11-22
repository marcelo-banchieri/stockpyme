from pydantic import BaseModel, ConfigDict, Field


class CategoriaCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)


class CategoriaLeer(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)