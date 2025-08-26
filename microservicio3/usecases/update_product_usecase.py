# domain/use_cases/update_product.py
from domain.entities.product import Product
from infrastructure.repositories.product_repository_api import ProductRepositoryAPI

class UpdateProduct:
    def __init__(self, repository: ProductRepositoryAPI):
        self.repository = repository

    def execute(self, sku: str, product: Product):
        return self.repository.update_product(sku, product)
