from datetime import datetime

from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=100)


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=100)
    rol: str | None = Field(default=None, max_length=50)


class UsuarioPublic(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    creado_en: datetime
