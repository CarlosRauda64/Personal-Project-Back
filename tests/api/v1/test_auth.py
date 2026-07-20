from tests.conftest import register_user


async def test_login_ok(client):
    await register_user(client)
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "vendedor@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


async def test_login_wrong_password(client):
    await register_user(client)
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "vendedor@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


async def test_login_unknown_user(client):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "noexiste@example.com", "password": "password123"},
    )
    assert response.status_code == 401
