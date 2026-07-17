def test_get_carros_empty(client):
    resp = client.get("/carros")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Lista de carros"
    assert data["carros"] == []


def test_create_carro(client):
    resp = client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "Carro criado com sucesso"
    assert data["carro"]["marca"] == "Fiat"


def test_create_carro_invalid_json(client):
    resp = client.post("/carros", data="not json", content_type="application/json")
    assert resp.status_code == 400


def test_create_carro_missing_field(client):
    resp = client.post("/carros", json={"marca": "Fiat"})
    assert resp.status_code == 400


def test_create_carro_invalid_ano(client):
    resp = client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 1800})
    assert resp.status_code == 400


def test_get_carros_with_data(client):
    client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010})
    resp = client.get("/carros")
    assert resp.status_code == 200
    assert len(resp.get_json()["carros"]) == 1


def test_update_carro(client):
    post_resp = client.post(
        "/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010}
    )
    carro_id = post_resp.get_json()["carro"]["id"]

    resp = client.put(
        f"/carros/{carro_id}", json={"marca": "Fiat", "modelo": "Palio", "ano": 2012}
    )
    assert resp.status_code == 200
    assert resp.get_json()["carro"]["modelo"] == "Palio"


def test_update_carro_not_found(client):
    resp = client.put(
        "/carros/999", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010}
    )
    assert resp.status_code == 404


def test_delete_carro(client):
    post_resp = client.post(
        "/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010}
    )
    carro_id = post_resp.get_json()["carro"]["id"]

    resp = client.delete(f"/carros/{carro_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Carro removido com sucesso"


def test_delete_carro_not_found(client):
    resp = client.delete("/carros/999")
    assert resp.status_code == 404


def test_get_carros_pagination(client):
    for i in range(15):
        client.post(
            "/carros", json={"marca": "Marca", "modelo": f"Modelo {i}", "ano": 2000 + i}
        )

    page1 = client.get("/carros?page=1&per_page=10")
    assert page1.status_code == 200
    data1 = page1.get_json()
    assert len(data1["carros"]) == 10
    assert data1["pagina"]["page"] == 1
    assert data1["pagina"]["per_page"] == 10
    assert data1["pagina"]["total"] == 15
    assert data1["pagina"]["pages"] == 2

    page2 = client.get("/carros?page=2&per_page=10")
    assert page2.status_code == 200
    assert len(page2.get_json()["carros"]) == 5


def test_get_carros_filtro_marca(client):
    client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010})
    client.post("/carros", json={"marca": "Ford", "modelo": "Focus", "ano": 2018})

    resp = client.get("/carros?marca=Fiat")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["carros"]) == 1
    assert data["carros"][0]["marca"] == "Fiat"


def test_get_carros_filtro_ano(client):
    client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010})
    client.post("/carros", json={"marca": "Fiat", "modelo": "Palio", "ano": 2012})

    resp = client.get("/carros?ano=2010")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["carros"]) == 1


def test_get_carros_filtro_modelo(client):
    client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010})
    client.post("/carros", json={"marca": "Fiat", "modelo": "Palio", "ano": 2012})

    resp = client.get("/carros?modelo=Uno")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["carros"]) == 1


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_get_carros_filtro_combinado(client):
    client.post("/carros", json={"marca": "Fiat", "modelo": "Uno", "ano": 2010})
    client.post("/carros", json={"marca": "Fiat", "modelo": "Palio", "ano": 2012})
    client.post("/carros", json={"marca": "Ford", "modelo": "Focus", "ano": 2010})

    resp = client.get("/carros?marca=Fiat&ano=2010")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data["carros"]) == 1
    assert data["carros"][0]["modelo"] == "Uno"
