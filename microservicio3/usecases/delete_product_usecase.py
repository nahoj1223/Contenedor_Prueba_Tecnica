from infrastructure.repositories.product_repository_api import ProductRepositoryAPI

class DeleteProductUseCase:
    def __init__(self, repository: ProductRepositoryAPI):
        self.repository = repository

    def execute(self, sku: str):
        return self.repository.delete_product(sku)
