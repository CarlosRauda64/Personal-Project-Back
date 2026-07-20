from fastapi import APIRouter

router = APIRouter(tags=["home"])


@router.get("/")
def home() -> dict:
    return {
        "nombre": "Personal Project API",
        "version": "0.1.0",
        "documentacion": {"swagger": "/docs", "redoc": "/redoc"},
        "endpoints": [
            {
                "metodo": "POST",
                "ruta": "/api/v1/auth/login",
                "descripcion": "Login (OAuth2, devuelve token JWT)",
                "requiere_auth": False,
            },
            {
                "metodo": "POST",
                "ruta": "/api/v1/users/",
                "descripcion": "Registrar usuario",
                "requiere_auth": False,
            },
            {
                "metodo": "GET",
                "ruta": "/api/v1/users/me",
                "descripcion": "Usuario autenticado",
                "requiere_auth": True,
            },
            {
                "metodo": "GET",
                "ruta": "/api/v1/users/",
                "descripcion": "Listar usuarios",
                "requiere_auth": True,
            },
            {
                "metodo": "GET",
                "ruta": "/api/v1/users/{user_id}",
                "descripcion": "Obtener usuario por id",
                "requiere_auth": True,
            },
            {
                "metodo": "PATCH",
                "ruta": "/api/v1/users/{user_id}",
                "descripcion": "Actualizar usuario",
                "requiere_auth": True,
            },
            {
                "metodo": "DELETE",
                "ruta": "/api/v1/users/{user_id}",
                "descripcion": "Eliminar usuario",
                "requiere_auth": True,
            },
        ],
    }
