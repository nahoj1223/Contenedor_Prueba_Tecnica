from fastapi.testclient import TestClient
from fastapi import FastAPI
from api.v1.pricing import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_quote_valid_product(monkeypatch):
    # Mock del caso de uso para simular respuesta exitosa
    class MockResponse:
        def __init__(self):
            self.sku = "550e8400-e29b-41d4-a716-446655440000"
            self.product_name = "Morral Totto"
            self.base_price = 120000
            self.iva = 19.00
            self.is_valid_country = True
            self.coupon = "SUMMER25"
            self.is_valid_coupon = True
            self.discount_coupon = 25.00
            self.final_price = 107100.00

    def mock_execute(self, db, pricing):
        return MockResponse()

    # Monkeypatch al método execute del caso de uso
    monkeypatch.setattr(
        "domain.use_cases.calculate_final_price.CalculateFinalPrice.execute",
        mock_execute
    )

    # Payload de prueba
    payload = {
        "sku": "550e8400-e29b-41d4-a716-446655440000",
        "country": "CO",
        "coupon": "SUMMER25"
    }

    # Llamada al endpoint
    response = client.post("/pricing/quote", json=payload)

    # Validaciones
    assert response.status_code == 200
    assert response.json()["product_name"] == "Morral Totto"
    assert response.json()["final_price"] == 107100.00


def test_quote_invalid_country(monkeypatch):
    # Mock del caso de uso para simular respuesta exitosa
    class MockResponse:
        def __init__(self):
            self.is_valid_country = False

    def mock_execute(self, db, pricing):
        return MockResponse()

    # Monkeypatch al método execute del caso de uso
    monkeypatch.setattr("domain.use_cases.calculate_final_price.CalculateFinalPrice.execute", mock_execute)

    # Payload de prueba
    payload = {
        "sku": "550e8400-e29b-41d4-a716-446655440000",
        "country": "KS",
        "coupon": "SUMMER25"
    }

    # Llamada al endpoint
    response = client.post("/pricing/quote", json=payload)

    # Validaciones
    assert response.status_code == 400
    assert "pais" in response.json()["detail"]

def test_quote_product_not_found(monkeypatch):
    # Mock del caso de uso para simular respuesta exitosa
    class MockResponse:
        def __init__(self):
            self.is_valid_country = True
            self.product_name = None

    def mock_execute(self, db, pricing):
        return MockResponse()

    # Monkeypatch al método execute del caso de uso
    monkeypatch.setattr("domain.use_cases.calculate_final_price.CalculateFinalPrice.execute", mock_execute)

    # Payload de prueba
    payload = {
        "sku": "550e8400-e29b-41d4-a716-446655440003",
        "country": "KS",
        "coupon": "SUMMER25"
    }

    # Llamada al endpoint
    response = client.post("/pricing/quote", json=payload)

    # Validaciones
    assert response.status_code == 404
    assert "producto" in response.json()["detail"]
