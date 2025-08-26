from domain.entities.product import Product
from infrastructure.repositories.product_repository_api import ProductRepositoryAPI

class GetProductUseCase:
    def __init__(self, repository: ProductRepositoryAPI):
        self.repository = repository

    def execute(self, sku: str) -> Product | None:
        return self.repository.get_product(sku)
