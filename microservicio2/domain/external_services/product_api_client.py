import requests
from domain.repositories.product_api_repository import ProductAPIRepository

class ProductAPIClient(ProductAPIRepository):
    BASE_URL = "http://microservicio1:8000"

    def get_product(self, sku: str) -> dict:
        response = requests.get(f"{self.BASE_URL}/products/{sku}")
        return response.json()