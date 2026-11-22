from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health_check_retorna_200():
    resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_criar_pedido_retorna_201_e_total_final():
    pedido = {"item": "Teclado", "valor": 150.0, "distancia_km": 10}

    resp = client.post("/pedidos", json=pedido)

    assert resp.status_code == 201
    assert resp.json()["total_final"] == 160.0


def test_criar_pedido_valor_negativo_retorna_400():
    pedido = {"item": "Mouse", "valor": -10.0, "distancia_km": 5}

    resp = client.post("/pedidos", json=pedido)

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Valor não pode ser negativo"


def test_criar_pedido_item_vazio_retorna_400():
    pedido = {"item": "", "valor": 50.0, "distancia_km": 5}

    resp = client.post("/pedidos", json=pedido)

    assert resp.status_code == 400


def test_listar_pedidos_mostra_pedido_criado():
    pedido = {"item": "Monitor", "valor": 80.0, "distancia_km": 2}
    criado = client.post("/pedidos", json=pedido).json()

    resp = client.get("/pedidos")

    assert resp.status_code == 200
    assert criado in resp.json()
