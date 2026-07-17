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
