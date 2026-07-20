from tests.conftest import get_token, register_user


async def test_create_user(client):
    response = await register_user(client)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "vendedor@example.com"
    assert data["nombre"] == "Usuario Test"
    assert data["rol"] == "vendedor"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


async def test_create_user_duplicate_email(client):
    await register_user(client)
    response = await register_user(client)
    assert response.status_code == 409


async def test_read_users_me(client):
    await register_user(client)
    token = await get_token(client, "vendedor@example.com", "password123")
    response = await client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "vendedor@example.com"


async def test_read_users_me_unauthorized(client):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


async def test_list_and_get_users(client):
    await register_user(client)
    token = await get_token(client, "vendedor@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1

    response = await client.get(f"/api/v1/users/{users[0]['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "vendedor@example.com"


async def test_update_and_delete_user(client):
    await register_user(client)
    token = await get_token(client, "vendedor@example.com", "password123")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.patch(
        "/api/v1/users/1", json={"nombre": "Nuevo Nombre"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == "Nuevo Nombre"

    response = await client.delete("/api/v1/users/1", headers=headers)
    assert response.status_code == 204

    # Con otro usuario autenticado, un id inexistente devuelve 404
    await register_user(client, email="admin@example.com", nombre="Admin Test")
    other_token = await get_token(client, "admin@example.com", "password123")
    response = await client.get(
        "/api/v1/users/999", headers={"Authorization": f"Bearer {other_token}"}
    )
    assert response.status_code == 404
