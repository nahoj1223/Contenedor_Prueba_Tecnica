from fastapi import HTTPException
from psycopg2 import IntegrityError
from fastapi.testclient import TestClient
from fastapi import FastAPI
from api.v1.product import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

#TEST CREATE PRODUCT
def test_create_product_success(monkeypatch):
    # Mock de la respuesta del caso de uso
    class MockProduct:
        sku = "prueba-sku"
        name = "prueba"
        base_price = 10
        currency = "COP"
        category = "varios"

    def mock_execute(self, db, product):
        return MockProduct()

    monkeypatch.setattr("domain.use_cases.create_product.CreateProduct.execute", mock_execute)

    payload = {
        "sku": "prueba-sku",
        "name": "prueba",
        "base_price": 10,
        "currency": "COP",
        "category": "varios"
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Product created"
    assert response.json()["product"]["sku"] == "prueba-sku"

def test_create_product_duplicate_sku(monkeypatch):
    def mock_execute(self, db, product):
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese SKU.")

    monkeypatch.setattr("domain.use_cases.create_product.CreateProduct.execute", mock_execute)

    payload = {
        "sku": "sku-repetido",
        "name": "Producto repetido",
        "base_price": 100,
        "currency": "COP",
        "category": "varios"
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Ya existe un producto con ese SKU."

def test_create_product_internal_error(monkeypatch):
    def mock_execute(self, db, product):
        raise Exception("Error inesperado")

    monkeypatch.setattr("domain.use_cases.create_product.CreateProduct.execute", mock_execute)

    payload = {
        "sku": "sku-error",
        "name": "Producto con error",
        "base_price": 200,
        "currency": "COP",
        "category": "otros"
    }

    response = client.post("/products", json=payload)

    assert response.status_code == 500
    assert "Error inesperado" in response.json()["detail"]

#TEST LIST PRODUCTS
def test_list_products_success(monkeypatch):
    class MockProduct:
        def __init__(self, sku, name):
            self.sku = sku
            self.name = name
            self.base_price = 100
            self.currency = "COP"
            self.category = "varios"

    def mock_execute(self, db):
        return [
            MockProduct("sku-1", "Producto 1"),
            MockProduct("sku-2", "Producto 2"),
        ]

    monkeypatch.setattr("domain.use_cases.list_products.ListProducts.execute", mock_execute)

    response = client.get("/products/list")

    assert response.status_code == 200
    body = response.json()
    assert body["cuantity"] == 2
    assert len(body["products"]) == 2
    assert body["products"][0]["sku"] == "sku-1"
    assert body["products"][1]["sku"] == "sku-2"

def test_list_products_empty(monkeypatch):
    def mock_execute(self, db):
        return []

    monkeypatch.setattr("domain.use_cases.list_products.ListProducts.execute", mock_execute)

    response = client.get("/products/list")

    assert response.status_code == 404
    assert response.json()["detail"] == "No hay productos"

def test_list_products_internal_error(monkeypatch):
    def mock_execute(self, db):
        raise Exception("Error inesperado")

    monkeypatch.setattr("domain.use_cases.list_products.ListProducts.execute", mock_execute)

    response = client.get("/products/list")

    assert response.status_code == 500
    assert "Error inesperado" in response.json()["detail"]

#TEST GET PRODUCT BY SKU
def test_get_product_success(monkeypatch):
    # Mock de la respuesta del caso de uso
    class MockProduct:
        def __init__(self):
            self.sku = "prueba-sku"
            self.name = "prueba"
            self.base_price = 10
            self.currency = "COP"
            self.category = "varios"

    def mock_execute(self, db, sku):
        return MockProduct()

    monkeypatch.setattr("domain.use_cases.get_product.GetProduct.execute", mock_execute)

    response = client.get("/products/prueba-sku")

    assert response.status_code == 200
    assert response.json()["name"] == "prueba"
    assert response.json()["base_price"]== 10

def test_get_product_not_found(monkeypatch):
    def mock_execute(self, db, sku):
        return None

    monkeypatch.setattr("domain.use_cases.get_product.GetProduct.execute", mock_execute)

    response = client.get("/products/sku-inexistente")

    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"

def test_get_product_internal_error(monkeypatch):
    def mock_execute(self, db, sku):
        raise Exception("Falla inesperada")

    monkeypatch.setattr("domain.use_cases.get_product.GetProduct.execute", mock_execute)

    response = client.get("/products/sku-error")

    assert response.status_code == 500
    assert "Falla" in response.json()["detail"]

#TEST UPDATE PRODUCT
def test_update_product_success(monkeypatch):
    class DummyProduct:
        def __init__(self):
            self.sku = "sku-existente"
            self.name = "Producto actualizado"
            self.base_price = 200
            self.currency = "COP"
            self.category = "varios"

    def mock_execute(self, db, sku, product):
        return DummyProduct()

    monkeypatch.setattr("domain.use_cases.put_product.UpdateProduct.execute", mock_execute)

    payload = {
        "name": "Producto actualizado",
        "base_price": 200,
        "currency": "COP",
        "category": "varios"
    }

    response = client.put("/products/sku-existente", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Product updated"
    assert body["product"]["sku"] == "sku-existente"
    assert body["product"]["name"] == "Producto actualizado"

def test_update_product_no_fields(monkeypatch):
    payload = {} 

    response = client.put("/products/sku-test", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "No se ha proporcionado ningun campo para actualizar"

def test_update_product_not_found(monkeypatch):
    def mock_execute(self, db, sku, product):
        class Dummy:
            sku = None
        return Dummy()

    monkeypatch.setattr("domain.use_cases.put_product.UpdateProduct.execute", mock_execute)

    payload = {"name": "Nuevo nombre"}

    response = client.put("/products/sku-inexistente", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"

def test_update_product_internal_error(monkeypatch):
    def mock_execute(self, db, sku, product):
        raise Exception("Error inesperado")

    monkeypatch.setattr("domain.use_cases.put_product.UpdateProduct.execute", mock_execute)

    payload = {"name": "Nuevo nombre"}

    response = client.put("/products/sku-test", json=payload)

    assert response.status_code == 500
    assert "Error inesperado" in response.json()["detail"]

#TEST DELETE PRODUCT
def test_delete_product_success(monkeypatch):
    def mock_execute(self, db, sku):
        return True  # Producto eliminado con éxito

    monkeypatch.setattr("domain.use_cases.delete_product.DeleteProduct.execute", mock_execute)

    response = client.delete("/products/sku-existente")

    assert response.status_code == 204
    assert response.content == b""  # 204 no devuelve cuerpo

def test_delete_product_not_found(monkeypatch):
    def mock_execute(self, db, sku):
        return False  # No se encontró

    monkeypatch.setattr("domain.use_cases.delete_product.DeleteProduct.execute", mock_execute)

    response = client.delete("/products/sku-inexistente")

    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"

def test_delete_product_internal_error(monkeypatch):
    def mock_execute(self, db, sku):
        raise Exception("Error inesperado")

    monkeypatch.setattr("domain.use_cases.delete_product.DeleteProduct.execute", mock_execute)

    response = client.delete("/products/sku-error")

    assert response.status_code == 500
    assert "Error inesperado" in response.json()["detail"]