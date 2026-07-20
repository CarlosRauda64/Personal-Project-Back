from sqlmodel import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import Usuario
from app.services import user_service

# Hash falso para verificar contraseñas cuando el usuario no existe
# y así mitigar ataques de temporización (timing attacks).
DUMMY_PASSWORD_HASH = get_password_hash("contrasena-falsa-para-timing")


def authenticate_user(session: Session, email: str, password: str) -> Usuario | None:
    user = user_service.get_user_by_email(session, email)
    if user is None:
        verify_password(password, DUMMY_PASSWORD_HASH)
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
