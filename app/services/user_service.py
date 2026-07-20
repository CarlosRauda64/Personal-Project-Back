from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.models.user import Usuario
from app.schemas.user import UsuarioCreate, UsuarioUpdate


def get_user_by_email(session: Session, email: str) -> Usuario | None:
    statement = select(Usuario).where(Usuario.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> Usuario | None:
    return session.get(Usuario, user_id)


def list_users(session: Session, offset: int = 0, limit: int = 100) -> list[Usuario]:
    statement = select(Usuario).offset(offset).limit(limit)
    return list(session.exec(statement).all())


def create_user(session: Session, user_in: UsuarioCreate) -> Usuario:
    if get_user_by_email(session, user_in.email) is not None:
        raise ValueError("Ya existe un usuario con ese email")
    user = Usuario(
        nombre=user_in.nombre,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user_id: int, user_in: UsuarioUpdate) -> Usuario | None:
    user = get_user_by_id(session, user_id)
    if user is None:
        return None
    data = user_in.model_dump(exclude_unset=True)
    if "email" in data:
        existing = get_user_by_email(session, data["email"])
        if existing is not None and existing.id != user_id:
            raise ValueError("Ya existe un usuario con ese email")
    if "password" in data:
        data["password_hash"] = get_password_hash(data.pop("password"))
    user.sqlmodel_update(data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = get_user_by_id(session, user_id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True
