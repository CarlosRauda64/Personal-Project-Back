from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str
    rol: str = Field(default="vendedor", max_length=50)
    creado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
