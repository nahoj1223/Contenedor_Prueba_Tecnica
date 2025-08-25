import requests

def test_integration_pricing_quote():
    #Creación de producto
    product_payload = {
        "sku": "prueba-sku",
        "name": "carpeta",
        "base_price": 180000,
        "currency": "COP",
        "category": "varios"
    }
    r = requests.post("http://microservicio1:8000/products", json=product_payload)
    assert r.status_code == 200

    #Calculo de precio final
    pricing_payload = {
        "sku": "prueba-sku",
        "country": "CO",
        "coupon": "BLACKFRIDAY"
    }
    r2 = requests.post("http://microservicio2:8001/pricing/quote", json=pricing_payload)
    assert r2.status_code == 200
    assert r2.json()["sku"] == "prueba-sku"
    assert r2.json()["product_name"] == "carpeta"

    #Eliminación de producto
    r = requests.delete("http://microservicio1:8000/products/prueba-sku")
    assert r.status_code == 204