async def test_home(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Personal Project API"
    assert data["documentacion"]["swagger"] == "/docs"
    rutas = [endpoint["ruta"] for endpoint in data["endpoints"]]
    assert "/api/v1/auth/login" in rutas
    assert "/api/v1/users/me" in rutas
