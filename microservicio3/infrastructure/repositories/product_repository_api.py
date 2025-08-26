import requests
from domain.entities.product import Product

class ProductRepositoryAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_product(self, product: Product):
        payload = {
            "sku": product.sku,
            "name": product.name,
            "base_price": product.base_price,
            "currency": product.currency,
            "category": product.category
        }
        response = requests.post(f"{self.base_url}/products", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error creando producto: {response.text}")
    
    def delete_product(self, sku: str):
        response = requests.delete(f"{self.base_url}/products/{sku}")
        if response.status_code == 204:
            return True
        elif response.status_code == 404:
            raise Exception("Producto no encontrado")
        else:
            raise Exception(f"Error eliminando producto: {response.text}")
    
    def get_product(self, sku: str) -> Product | None:
        response = requests.get(f"{self.base_url}/products/{sku}")
        if response.status_code == 200:
            return Product(**response.json())
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()

    def list_product(self) -> list | None:
        response = requests.get(f"{self.base_url}/products/list")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()