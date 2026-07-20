from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.dependencies import CurrentUserDep
from app.core.database import SessionDep
from app.schemas.user import UsuarioCreate, UsuarioPublic, UsuarioUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(session: SessionDep, user_in: UsuarioCreate) -> UsuarioPublic:
    try:
        return user_service.create_user(session, user_in)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error


@router.get("/me", response_model=UsuarioPublic)
def read_users_me(current_user: CurrentUserDep) -> UsuarioPublic:
    return current_user


@router.get("/")
def list_users(
    session: SessionDep,
    current_user: CurrentUserDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[UsuarioPublic]:
    return user_service.list_users(session, offset=offset, limit=limit)


@router.get("/{user_id}")
def get_user(
    session: SessionDep, current_user: CurrentUserDep, user_id: int
) -> UsuarioPublic:
    user = user_service.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return user


@router.patch("/{user_id}")
def update_user(
    session: SessionDep, current_user: CurrentUserDep, user_id: int, user_in: UsuarioUpdate
) -> UsuarioPublic:
    try:
        user = user_service.update_user(session, user_id, user_in)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: SessionDep, current_user: CurrentUserDep, user_id: int) -> None:
    if not user_service.delete_user(session, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
