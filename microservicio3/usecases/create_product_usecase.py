from domain.entities.product import Product
from infrastructure.repositories.product_repository_api import ProductRepositoryAPI

class CreateProductUseCase:
    def __init__(self, repository: ProductRepositoryAPI):
        self.repository = repository

    def execute(self, product: Product):
        return self.repository.create_product(product)